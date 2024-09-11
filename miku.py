
import os
import time
import json
import base64
import hashlib
from io import BytesIO
from PIL import Image as PIL_Image
from db import db, Image, Path, Tag
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gallery.db'
db.init_app(app)

def get_bit_depth(image):
    mode_to_bpp = {
        '1': 1,  # 1-bit pixels, black and white
        'L': 8,  # 8-bit pixels, grayscale
        'P': 8,  # 8-bit pixels, mapped to any other mode using a color palette
        'RGB': 24,  # 3x8-bit pixels, true color
        'RGBA': 32,  # 4x8-bit pixels, true color with transparency mask
        'CMYK': 32,  # 4x8-bit pixels, color separation
        'YCbCr': 24,  # 3x8-bit pixels, color video format
        'LAB': 24,  # 3x8-bit pixels, the L*a*b color space
        'HSV': 24,  # 3x8-bit pixels, Hue, Saturation, Value color space
        'I': 32,  # 32-bit signed integer pixels
        'F': 32,  # 32-bit floating point pixels
    }
    return mode_to_bpp.get(image.mode, 0)

def convert_bytes_to_str(data):
    if isinstance(data, bytes):
        return base64.b64encode(data).decode('utf-8')  # Convert bytes to base64 encoded string
    elif isinstance(data, dict):
        return {k: convert_bytes_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_bytes_to_str(v) for v in data]
    else:
        return data

def scan_directory(path):
    #print(path, "bip bip bip")
    for root, dirs, files in os.walk(path):
        for directory in [*dirs, path]:
            #print(path, 1)
            #print(dir(path))
            path = os.path.join(root, directory)
            if Path.query.filter_by(path=path).first():
                continue
            
            #print(path)
            
            db.session.add(Path(path=path))
            db.session.commit()
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp')):
                file_path = os.path.join(root, file)
                filename = os.path.basename(file_path)
                
                directory = Path.query.filter_by(path=os.path.dirname(file_path)).first()
                
                if Image.query.filter_by(filename=filename, path=directory).first():
                    continue
            
                with PIL_Image.open(file_path) as img:
                    hash = hashlib.md5(img.tobytes()).hexdigest()
                    file_size = os.path.getsize(file_path)
                    bit_depth = get_bit_depth(img)
                    
                    new_image = Image(path=directory, filename=filename, hash=hash, file_size=file_size, width=img.width,
                                      height=img.height, file_type=img.format, bit_depth=bit_depth)
                    
                    db.session.add(new_image)
                    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    print(Path.query.all())
    if not Path.query.all():
        return redirect('/config')
        # return render_template('config.html')
    return render_template('index.html')

@app.route('/load_images', methods=['GET'])
def load_images():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 20))
    images = Image.query.offset(offset).limit(limit).all()
    return jsonify([{
        'hash':image.hash,
        'filename': image.filename
    } for image in images])

@app.route('/images/<hash>')
def serve_image(hash):
    image_record = Image.query.filter_by(hash=hash).first()
    if image_record:
        return send_from_directory(image_record.path.path, image_record.filename)
    
    return "Image not found", 404

@app.route('/reload/<path>')
def reload_path(path):
    print(base64.b64decode(path).decode())
    scan_directory(base64.b64decode(path).decode())
    return render_template('index.html')

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        path = request.form.get('path')
        if path:
            if Path.query.filter_by(path=path).first():
                return f'''Le chemin {path} existe déjà dans la bdd.<br>
            Voulez-vous actualiser les fichiers ?<br>
            <button onclick="window.location.href='/reload/{base64.b64encode(path.encode('utf-8')).decode()}';">oui</button>
            <button onclick="window.location = window.location.href;">non</button>
            '''
            
            scan_directory(path)
            return redirect("/")
    return render_template('config.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

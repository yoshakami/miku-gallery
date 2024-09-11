from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def paths():
    return ["C:\\Users\\yoshi\\Pictures\\anime"]


class ImageMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)
    file_name = db.Column(db.String, nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String, nullable=False)
    bit_depth = db.Column(db.Integer, nullable=False)
    image_metadata = db.Column(db.Text, nullable=True)  # Store JSON as text

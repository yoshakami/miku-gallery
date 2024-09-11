from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Path(db.Model):
    __tablename__ = "path"
    
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, unique=True, nullable=False)
    
    images = db.relationship("Image", back_populates="path")

image_tag = db.Table(
    "image_tag",
    db.Column("image", db.ForeignKey("image.id"), primary_key=True),
    db.Column("tag", db.ForeignKey("tag.name"), primary_key=True),
)

class Image(db.Model):
    __tablename__ = "image"
    
    id = db.Column(db.Integer, primary_key=True)
    path_id = db.Column(db.Integer, db.ForeignKey("path.id"))
    path = db.relationship("Path", back_populates="images")

    hash = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String, nullable=False)
    bit_depth = db.Column(db.Integer, nullable=False)
    
    tags = db.relationship("Tag", secondary=image_tag, back_populates="images") 
    
class Tag(db.Model):
    __tablename__ = "tag"
    
    name = db.Column(db.String, primary_key=True)
    
    images = db.relationship("Image", secondary=image_tag, back_populates="tags")

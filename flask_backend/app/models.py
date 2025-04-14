from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# 创建SQLAlchemy实例
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user'), nullable=False, default='user')
    email = db.Column(db.String(100))
    region = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'role': self.role,
            'email': self.email,
            'region': self.region,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class CropCategory(db.Model):
    __tablename__ = 'crop_categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    update_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联病害
    diseases = db.relationship('Disease', backref='category', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }

class Disease(db.Model):
    __tablename__ = 'diseases'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(100), nullable=False)
    name_zh = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('crop_categories.id'))
    description = db.Column(db.Text)
    symptoms = db.Column(db.Text)
    treatment = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    create_time = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    update_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name_zh': self.name_zh,
            'name_en': self.name_en,
            'category_id': self.category_id,
            'description': self.description,
            'symptoms': self.symptoms,
            'treatment': self.treatment,
            'image_url': self.image_url,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        } 
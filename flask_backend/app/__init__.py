from flask import Flask
from flask_jwt_extended import JWTManager
from .config import Config
from .models import db
from .routes.auth import auth_bp
from .routes.category import category_bp
from .routes.disease import disease_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    jwt = JWTManager(app)
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(disease_bp, url_prefix='/api/diseases')
    
    return app 
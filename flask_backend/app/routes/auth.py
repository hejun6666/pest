from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from ..models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 检查必要字段
    if not all(k in data for k in ('username', 'password')):
        return jsonify({'msg': '缺少必要字段'}), 400
        
    # 检查用户名是否存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'msg': '用户名已存在'}), 400
    
    # 创建新用户
    user = User(
        username=data['username'],
        email=data.get('email'),
        region=data.get('region'),
        role='user'  # 默认为普通用户
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'msg': '注册成功', 'user_id': user.user_id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 检查必要字段
    if not all(k in data for k in ('username', 'password')):
        return jsonify({'msg': '缺少必要字段'}), 400
    
    # 查找用户
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'msg': '用户名或密码错误'}), 401
    
    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # 创建访问令牌
    access_token = create_access_token(identity=user.user_id)
    return jsonify({
        'access_token': access_token, 
        'user': user.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
        
    return jsonify(user.to_dict()), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
    
    data = request.get_json()
    
    # 更新用户信息
    if 'email' in data:
        user.email = data['email']
    if 'region' in data:
        user.region = data['region']
    if 'password' in data:
        user.set_password(data['password'])
    
    db.session.commit()
    return jsonify({'msg': '更新成功', 'user': user.to_dict()}), 200 
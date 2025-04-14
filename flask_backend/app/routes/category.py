from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, User, CropCategory

category_bp = Blueprint('category', __name__)

# 检查管理员权限的函数
def is_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.role == 'admin'

@category_bp.route('', methods=['GET'])
def get_categories():
    categories = CropCategory.query.all()
    return jsonify([category.to_dict() for category in categories]), 200

@category_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    category = CropCategory.query.get_or_404(id)
    return jsonify(category.to_dict()), 200

@category_bp.route('', methods=['POST'])
@jwt_required()
def create_category():
    # 检查管理员权限
    if not is_admin():
        return jsonify({'msg': '权限不足'}), 403
    
    data = request.get_json()
    
    # 检查必要字段
    if not all(k in data for k in ('name', 'code')):
        return jsonify({'msg': '缺少必要字段'}), 400
    
    # 检查代码是否存在
    if CropCategory.query.filter_by(code=data['code']).first():
        return jsonify({'msg': '分类代码已存在'}), 400
    
    category = CropCategory(
        name=data['name'],
        code=data['code']
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({'msg': '创建成功', 'category': category.to_dict()}), 201

@category_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    # 检查管理员权限
    if not is_admin():
        return jsonify({'msg': '权限不足'}), 403
    
    category = CropCategory.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data:
        category.name = data['name']
    if 'code' in data:
        # 检查代码是否存在
        existing = CropCategory.query.filter_by(code=data['code']).first()
        if existing and existing.id != id:
            return jsonify({'msg': '分类代码已存在'}), 400
        category.code = data['code']
    
    db.session.commit()
    return jsonify({'msg': '更新成功', 'category': category.to_dict()}), 200

@category_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    # 检查管理员权限
    if not is_admin():
        return jsonify({'msg': '权限不足'}), 403
    
    category = CropCategory.query.get_or_404(id)
    
    # 检查该分类下是否有病害
    if category.diseases.count() > 0:
        return jsonify({'msg': '该分类下存在病害记录，无法删除'}), 400
    
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'msg': '删除成功'}), 200 
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, User, Disease, CropCategory

disease_bp = Blueprint('disease', __name__)

# 检查管理员权限的函数
def is_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.role == 'admin'

@disease_bp.route('', methods=['GET'])
def get_diseases():
    # 获取查询参数
    category_id = request.args.get('category_id', type=int)
    
    query = Disease.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    diseases = query.all()
    return jsonify([disease.to_dict() for disease in diseases]), 200

@disease_bp.route('/<int:id>', methods=['GET'])
def get_disease(id):
    disease = Disease.query.get_or_404(id)
    return jsonify(disease.to_dict()), 200

@disease_bp.route('', methods=['POST'])
@jwt_required()
def create_disease():
    # 检查管理员权限
    if not is_admin():
        return jsonify({'msg': '权限不足'}), 403
    
    data = request.get_json()
    
    # 检查必要字段
    if not all(k in data for k in ('code', 'name_zh', 'name_en')):
        return jsonify({'msg': '缺少必要字段'}), 400
    
    # 检查代码是否存在
    if Disease.query.filter_by(code=data['code']).first():
        return jsonify({'msg': '病害代码已存在'}), 400
    
    # 检查分类是否存在
    if 'category_id' in data and data['category_id']:
        category = CropCategory.query.get(data['category_id'])
        if not category:
            return jsonify({'msg': '分类不存在'}), 400
    
    disease = Disease(
        code=data['code'],
        name_zh=data['name_zh'],
        name_en=data['name_en'],
        category_id=data.get('category_id'),
        description=data.get('description'),
        symptoms=data.get('symptoms'),
        treatment=data.get('treatment'),
        image_url=data.get('image_url')
    )
    
    db.session.add(disease)
    db.session.commit()
    
    return jsonify({'msg': '创建成功', 'disease': disease.to_dict()}), 201

@disease_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_disease(id):
    # 检查管理员权限
    if not is_admin():
        return jsonify({'msg': '权限不足'}), 403
    
    disease = Disease.query.get_or_404(id)
    data = request.get_json()
    
    # 更新字段
    if 'code' in data:
        existing = Disease.query.filter_by(code=data['code']).first()
        if existing and existing.id != id:
            return jsonify({'msg': '病害代码已存在'}), 400
        disease.code = data['code']
    
    if 'name_zh' in data:
        disease.name_zh = data['name_zh']
    if 'name_en' in data:
        disease.name_en = data['name_en']
    if 'category_id' in data:
        if data['category_id']:
            category = CropCategory.query.get(data['category_id'])
            if not category:
                return jsonify({'msg': '分类不存在'}), 400
        disease.category_id = data['category_id']
    if 'description' in data:
        disease.description = data['description']
    if 'symptoms' in data:
        disease.symptoms = data['symptoms']
    if 'treatment' in data:
        disease.treatment = data['treatment']
    if 'image_url' in data:
        disease.image_url = data['image_url']
    
    db.session.commit()
    return jsonify({'msg': '更新成功', 'disease': disease.to_dict()}), 200

@disease_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_disease(id):
    # 检查管理员权限
    if not is_admin():
        return jsonify({'msg': '权限不足'}), 403
    
    disease = Disease.query.get_or_404(id)
    
    db.session.delete(disease)
    db.session.commit()
    
    return jsonify({'msg': '删除成功'}), 200 
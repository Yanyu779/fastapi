from flask import Blueprint, request, jsonify
from app import db
from app.models import User

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': '名字和邮箱是必填项'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '邮箱已存在'}), 400
    
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '无效的数据'}), 400
    
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': '邮箱已被其他用户使用'}), 400
        user.email = data['email']
    
    db.session.commit()
    return jsonify(user.to_dict())

@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': '用户已删除'})
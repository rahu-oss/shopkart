from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.cart import Cart
from models.product import Product
from models.user import User
from database.db import db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        user_id = get_jwt_identity()
        
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        
        total_price = sum(item.product.price * item.quantity for item in cart_items if item.product)
        total_items = sum(item.quantity for item in cart_items)
        
        return {
            'cart_items': [item.to_dict() for item in cart_items],
            'total_items': total_items,
            'total_price': total_price
        }, 200
    
    except Exception as e:
        return {'error': str(e)}, 500

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('product_id'):
            return {'error': 'Product ID is required'}, 400
        
        product = Product.query.get(data['product_id'])
        if not product:
            return {'error': 'Product not found'}, 404
        
        if product.stock <= 0:
            return {'error': 'Product is out of stock'}, 400
        
        quantity = data.get('quantity', 1)
        
        # Check if product already in cart
        cart_item = Cart.query.filter_by(
            user_id=user_id,
            product_id=data['product_id']
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = Cart(
                user_id=user_id,
                product_id=data['product_id'],
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        return {
            'message': 'Product added to cart',
            'cart_item': cart_item.to_dict()
        }, 200
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@cart_bp.route('/<int:cart_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(cart_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        cart_item = Cart.query.filter_by(
            id=cart_id,
            user_id=user_id
        ).first()
        
        if not cart_item:
            return {'error': 'Cart item not found'}, 404
        
        quantity = data.get('quantity', 1)
        
        if quantity <= 0:
            db.session.delete(cart_item)
        else:
            if cart_item.product.stock < quantity:
                return {'error': 'Insufficient stock'}, 400
            cart_item.quantity = quantity
        
        db.session.commit()
        
        return {
            'message': 'Cart item updated',
            'cart_item': cart_item.to_dict() if quantity > 0 else None
        }, 200
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@cart_bp.route('/<int:cart_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(cart_id):
    try:
        user_id = get_jwt_identity()
        
        cart_item = Cart.query.filter_by(
            id=cart_id,
            user_id=user_id
        ).first()
        
        if not cart_item:
            return {'error': 'Cart item not found'}, 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return {'message': 'Item removed from cart'}, 200
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    try:
        user_id = get_jwt_identity()
        
        Cart.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return {'message': 'Cart cleared successfully'}, 200
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

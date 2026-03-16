from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.order import Order, OrderItem
from models.cart import Cart
from models.product import Product
from models.user import User
from database.db import db
from datetime import datetime
import random
import string

order_bp = Blueprint('orders', __name__)

def generate_order_number():
    """Generate a unique order number"""
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"ORD-{datetime.now().strftime('%Y%m%d')}-{random_str}"

@order_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        # Get cart items
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        
        if not cart_items:
            return {'error': 'Cart is empty'}, 400
        
        data = request.get_json()
        
        # Calculate totals
        total_amount = 0
        total_discount = 0
        
        for item in cart_items:
            if not item.product or item.product.stock < item.quantity:
                return {'error': f'Insufficient stock for {item.product.name}'}, 400
            
            item_total = item.product.price * item.quantity
            total_amount += item_total
            total_discount += (item.product.discount or 0) * item.quantity
        
        # Tax calculation (assuming 18% GST)
        tax = total_amount * 0.18
        final_amount = total_amount - total_discount + tax
        
        # Create order
        order = Order(
            user_id=user_id,
            order_number=generate_order_number(),
            total_amount=total_amount,
            discount=total_discount,
            tax=tax,
            final_amount=final_amount,
            payment_method=data.get('payment_method', 'cod'),
            shipping_address=data.get('shipping_address', user.address),
            status='pending',
            payment_status='pending'
        )
        
        # Create order items and reduce stock
        for item in cart_items:
            order_item = OrderItem(
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.product.price,
                total=item.product.price * item.quantity
            )
            
            # Reduce stock
            item.product.stock -= item.quantity
            
            order.items.append(order_item)
        
        db.session.add(order)
        
        # Clear cart
        Cart.query.filter_by(user_id=user_id).delete()
        
        db.session.commit()
        
        return {
            'message': 'Order created successfully',
            'order': order.to_dict()
        }, 201
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@order_bp.route('', methods=['GET'])
@jwt_required()
def get_user_orders():
    try:
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        orders = Order.query.filter_by(user_id=user_id).order_by(
            Order.created_at.desc()
        ).paginate(page=page, per_page=per_page)
        
        return {
            'orders': [o.to_dict() for o in orders.items],
            'total': orders.total,
            'pages': orders.pages
        }, 200
    
    except Exception as e:
        return {'error': str(e)}, 500

@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    try:
        user_id = get_jwt_identity()
        
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return {'error': 'Order not found'}, 404
        
        return {'order': order.to_dict()}, 200
    
    except Exception as e:
        return {'error': str(e)}, 500

@order_bp.route('/<int:order_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_order(order_id):
    try:
        user_id = get_jwt_identity()
        
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return {'error': 'Order not found'}, 404
        
        if order.status not in ['pending', 'confirmed']:
            return {'error': 'Cannot cancel this order'}, 400
        
        # Restore stock
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity
        
        order.status = 'cancelled'
        db.session.commit()
        
        return {
            'message': 'Order cancelled successfully',
            'order': order.to_dict()
        }, 200
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@order_bp.route('/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    try:
        order = Order.query.get(order_id)
        
        if not order:
            return {'error': 'Order not found'}, 404
        
        data = request.get_json()
        
        order.status = data.get('status', order.status)
        order.payment_status = data.get('payment_status', order.payment_status)
        order.tracking_number = data.get('tracking_number', order.tracking_number)
        
        db.session.commit()
        
        return {
            'message': 'Order status updated',
            'order': order.to_dict()
        }, 200
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@order_bp.route('/search/<order_number>', methods=['GET'])
@jwt_required()
def search_order(order_number):
    try:
        user_id = get_jwt_identity()
        
        order = Order.query.filter_by(
            order_number=order_number,
            user_id=user_id
        ).first()
        
        if not order:
            return {'error': 'Order not found'}, 404
        
        return {'order': order.to_dict()}, 200
    
    except Exception as e:
        return {'error': str(e)}, 500

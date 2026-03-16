from flask import Blueprint, request, jsonify
from models.product import Product
from database.db import db
from sqlalchemy import or_, and_

product_bp = Blueprint('products', __name__)


# ✅ GET ALL PRODUCTS
@product_bp.route('/', methods=['GET'])
def get_products():
    try:

        category = request.args.get('category')
        search = request.args.get('search')
        sort = request.args.get('sort', 'name')
        order = request.args.get('order', 'asc')

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        query = Product.query.filter_by(is_active=True)

        # Category filter
        if category:
            query = query.filter_by(category=category)

        # Search filter
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.description.ilike(f'%{search}%')
                )
            )

        # Sorting
        if sort == 'price':

            if order == 'asc':
                query = query.order_by(Product.price.asc())
            else:
                query = query.order_by(Product.price.desc())

        elif sort == 'rating':

            if order == 'asc':
                query = query.order_by(Product.rating.asc())
            else:
                query = query.order_by(Product.rating.desc())

        else:

            if order == 'asc':
                query = query.order_by(Product.name.asc())
            else:
                query = query.order_by(Product.name.desc())

        # ⭐ FIXED PAGINATION
        products = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return jsonify({

            "products": [p.to_dict() for p in products.items],

            "total": products.total,

            "pages": products.pages,

            "current_page": page

        }), 200


    except Exception as e:

        print("ERROR:", e)

        return jsonify({

            "error": str(e)

        }), 500



# ✅ GET SINGLE PRODUCT
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):

    try:

        product = Product.query.get(product_id)

        if not product:

            return jsonify({

                "error": "Product not found"

            }), 404


        return jsonify({

            "product": product.to_dict()

        }), 200


    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500



# ✅ GET BY CATEGORY
@product_bp.route('/category/<category>', methods=['GET'])
def get_products_by_category(category):

    try:

        page = request.args.get('page', 1, type=int)

        per_page = request.args.get('per_page', 10, type=int)


        products = Product.query.filter_by(

            category=category,
            is_active=True

        ).paginate(

            page=page,
            per_page=per_page,
            error_out=False   # ⭐ FIX

        )


        return jsonify({

            "category": category,

            "products": [p.to_dict() for p in products.items],

            "total": products.total,

            "pages": products.pages

        }), 200


    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500




# ✅ SEARCH PRODUCTS
@product_bp.route('/search/<query>', methods=['GET'])
def search_products(query):

    try:

        page = request.args.get('page', 1, type=int)

        per_page = request.args.get('per_page', 10, type=int)


        products = Product.query.filter(

            and_(

                Product.is_active == True,

                or_(

                    Product.name.ilike(f'%{query}%'),

                    Product.description.ilike(f'%{query}%')

                )

            )

        ).paginate(

            page=page,
            per_page=per_page,
            error_out=False   # ⭐ FIX

        )


        return jsonify({

            "search_query": query,

            "products": [p.to_dict() for p in products.items],

            "total": products.total,

            "pages": products.pages

        }), 200


    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500




# ✅ CREATE PRODUCT
@product_bp.route('/', methods=['POST'])
def create_product():

    try:

        data = request.get_json()

        if not data.get("name") or not data.get("price"):

            return jsonify({

                "error": "Name and price required"

            }), 400


        product = Product(

            name=data["name"],

            description=data.get("description"),

            price=data["price"],

            original_price=data.get("original_price", data["price"]),

            discount=data.get("discount", 0),

            stock=data.get("stock", 0),

            category=data.get("category"),

            image_url=data.get("image_url"),

            seller=data.get("seller", "Admin"),

            rating=data.get("rating", 0)

        )


        db.session.add(product)

        db.session.commit()


        return jsonify({

            "message": "Product created",

            "product": product.to_dict()

        }), 201


    except Exception as e:

        db.session.rollback()

        return jsonify({

            "error": str(e)

        }), 500




# ✅ UPDATE PRODUCT
@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):

    try:

        product = Product.query.get(product_id)

        if not product:

            return jsonify({

                "error": "Product not found"

            }), 404


        data = request.get_json()


        product.name = data.get("name", product.name)

        product.price = data.get("price", product.price)

        product.stock = data.get("stock", product.stock)

        product.category = data.get("category", product.category)


        db.session.commit()


        return jsonify({

            "message": "Product updated",

            "product": product.to_dict()

        })


    except Exception as e:

        db.session.rollback()

        return jsonify({

            "error": str(e)

        }), 500




# ✅ DELETE PRODUCT
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):

    try:

        product = Product.query.get(product_id)

        if not product:

            return jsonify({

                "error": "Product not found"

            }), 404


        db.session.delete(product)

        db.session.commit()


        return jsonify({

            "message": "Product deleted"

        })


    except Exception as e:

        db.session.rollback()

        return jsonify({

            "error": str(e)

        }), 500

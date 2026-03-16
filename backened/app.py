from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

app = Flask(__name__)

# Configuration
database_url = os.environ.get('postgresql://shopkart_product_database_user:sNAddlskRxHaNJv3saNBnr2GwHq5HVSU@dpg-d6s4hfnpm1nc73dub55g-a/shopkart_product_database')
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopkart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '0s1h2o2s3h4o5s6h7o8s9h0o1s2h3o4s5h6o7s8h9o0s1h2o3s4h5o6s7h8o9s0h1o2s3h4o5s6h7o8s9h0o1s2h3o4s5h6o7s8h9o0'  # Change this to a secure key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
jwt = JWTManager(app)

# Import database
from database.db import db
db.init_app(app)

# Allow both trailing and non-trailing slashes to avoid redirects (helps CORS preflight)
app.url_map.strict_slashes = False

# Import routes
from routes.auth import auth_bp
from routes.product import product_bp
from routes.cart import cart_bp
from routes.order import order_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(product_bp, url_prefix='/api/products')
app.register_blueprint(cart_bp, url_prefix='/api/cart')
app.register_blueprint(order_bp, url_prefix='/api/orders')

# Create tables
with app.app_context():
    db.create_all()
@app.route("/")
def home():

    return "ShopKart Backend Running Successfully"

@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'Server is running', 'message': 'ShopKart API'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

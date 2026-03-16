"""
Script to add sample products to the database
Run this after starting the Flask app
"""

from app import app
from database.db import db
from models.product import Product

# Sample products data
PRODUCTS = [
    {
        "name": "iPhone 15 Pro",
        "description": "Latest Apple iPhone with advanced camera system",
        "price": 79999,
        "original_price": 84999,
        "discount": 5,
        "stock": 50,
        "category": "electronics",
        "image_url": "https://via.placeholder.com/250?text=iPhone+15",
        "seller": "Apple Store",
        "rating": 4.8,
        "reviews_count": 1250
    },
    {
        "name": "Sony WH-1000XM5 Headphones",
        "description": "Premium noise-cancelling wireless headphones",
        "price": 29999,
        "original_price": 34999,
        "discount": 14,
        "stock": 100,
        "category": "electronics",
        "image_url": "https://via.placeholder.com/250?text=Sony+Headphones",
        "seller": "Sony",
        "rating": 4.6,
        "reviews_count": 2100
    },
    {
        "name": "Nike Running Shoes",
        "description": "Comfortable and durable running shoes",
        "price": 8999,
        "original_price": 12999,
        "discount": 30,
        "stock": 150,
        "category": "clothing",
        "image_url": "https://via.placeholder.com/250?text=Nike+Shoes",
        "seller": "Nike",
        "rating": 4.5,
        "reviews_count": 1500
    },
    {
        "name": "Harry Potter Book Series",
        "description": "Complete collection of all 7 Harry Potter books",
        "price": 1999,
        "original_price": 2499,
        "discount": 20,
        "stock": 200,
        "category": "books",
        "image_url": "https://via.placeholder.com/250?text=Harry+Potter",
        "seller": "Penguin Books",
        "rating": 4.9,
        "reviews_count": 5000
    },
    {
        "name": "Wooden Dining Table",
        "description": "Premium quality wooden dining table for 6 people",
        "price": 24999,
        "original_price": 34999,
        "discount": 28,
        "stock": 20,
        "category": "home",
        "image_url": "https://via.placeholder.com/250?text=Dining+Table",
        "seller": "Furniture Hub",
        "rating": 4.4,
        "reviews_count": 320
    },
    {
        "name": "Badminton Racket Set",
        "description": "Professional badminton racket set with shuttles",
        "price": 2999,
        "original_price": 4999,
        "discount": 40,
        "stock": 80,
        "category": "sports",
        "image_url": "https://via.placeholder.com/250?text=Badminton+Set",
        "seller": "Sports World",
        "rating": 4.3,
        "reviews_count": 450
    },
    {
        "name": "LEGO Technic Robot",
        "description": "Advanced LEGO Technic building set with motor",
        "price": 3499,
        "original_price": 5499,
        "discount": 36,
        "stock": 60,
        "category": "toys",
        "image_url": "https://via.placeholder.com/250?text=LEGO+Robot",
        "seller": "LEGO Store",
        "rating": 4.7,
        "reviews_count": 890
    },
]

def add_products():
    """Add sample products to database"""
    with app.app_context():
        # Check if products already exist
        existing = Product.query.first()
        if existing:
            print("Products already exist in database!")
            return
        
        # Add each product
        for product_data in PRODUCTS:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print(f"✅ Successfully added {len(PRODUCTS)} products to database!")
        
        # Display added products
        products = Product.query.all()
        print("\nProducts in database:")
        for p in products:
            print(f"  - {p.name} (ID: {p.id}, ₹{p.price})")

if __name__ == "__main__":
    add_products()

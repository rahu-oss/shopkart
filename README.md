#!/bin/bash

# ShopKart E-Commerce Backend Setup Guide

## Installation Steps

### 1. Navigate to Project Directory
cd backened

### 2. Create Virtual Environment
python -m venv venv

### 3. Activate Virtual Environment

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

### 4. Install Dependencies
pip install -r requirements.txt

### 5. Run the Application
python app.py

The server will run at http://localhost:5000

## API Endpoints

### Authentication Routes
- POST   /api/auth/register        - Register new user
- POST   /api/auth/login           - Login user
- GET    /api/auth/profile         - Get user profile (Requires JWT)
- PUT    /api/auth/profile         - Update user profile (Requires JWT)

### Product Routes
- GET    /api/products             - Get all products (with filters, search, sort, pagination)
- GET    /api/products/:id         - Get product by ID
- GET    /api/products/category/:category - Get products by category
- GET    /api/products/search/:query - Search products
- POST   /api/products             - Create product
- PUT    /api/products/:id         - Update product
- DELETE /api/products/:id         - Delete product

### Cart Routes
- GET    /api/cart                 - Get user's cart (Requires JWT)
- POST   /api/cart/add             - Add product to cart (Requires JWT)
- PUT    /api/cart/:id             - Update cart item quantity (Requires JWT)
- DELETE /api/cart/:id             - Remove item from cart (Requires JWT)
- DELETE /api/cart/clear           - Clear entire cart (Requires JWT)

### Order Routes
- POST   /api/orders               - Create order (Requires JWT)
- GET    /api/orders               - Get user's orders (Requires JWT)
- GET    /api/orders/:id           - Get order by ID (Requires JWT)
- PUT    /api/orders/:id/cancel    - Cancel order (Requires JWT)
- PUT    /api/orders/:id/status    - Update order status (Admin)
- GET    /api/orders/search/:order_number - Search order by number (Requires JWT)

## Database Models

### User
- id, username, email, password_hash, first_name, last_name, phone, address, city, state, pincode, created_at, updated_at

### Product
- id, name, description, price, original_price, discount, stock, category, image_url, rating, reviews_count, seller, is_active, created_at, updated_at

### Cart
- id, user_id, product_id, quantity, created_at, updated_at

### Order
- id, user_id, order_number, total_amount, discount, tax, final_amount, status, payment_method, payment_status, shipping_address, tracking_number, created_at, updated_at

### OrderItem
- id, order_id, product_id, product_name, quantity, price, total

## Features

✓ User Authentication (Register/Login with JWT)
✓ Product Management (CRUD operations)
✓ Product Search and Filtering
✓ Shopping Cart Management
✓ Order Management
✓ Stock Management
✓ Order Tracking
✓ Multiple Payment Methods (COD, Credit Card, Debit Card, UPI, Wallet)
✓ Order Status Management
✓ User Profile Management
✓ Pagination and Sorting
✓ Admin Product Management
✓ Discount and Tax Calculation

## Technology Stack
- Framework: Flask
- Database: SQLite (can be changed to MySQL/PostgreSQL)
- Authentication: Flask-JWT-Extended
- ORM: SQLAlchemy
- CORS: Flask-CORS

from app import app
from database.db import db
from models.product import Product


def main():



    product_images = [

        {
            "name": "iPhone 15",
            "image_url": "/static/images/product1.webp"
        },

        {
            "name": "Samsung Galaxy S24",
            "image_url": "/static/images/product2.webp"
        },

        {
            "name": "Shoes",
            "image_url": "/static/images/shoes.webp"
        },

        {
            "name": "Watch",
            "image_url": "/static/images/watch.webp"
        }

    ]


    with app.app_context():

        for item in product_images:

            product = Product.query.filter_by(name=item["name"]).first()

            if product:

                product.image_url = item["image_url"]

                print(f"✅ Updated: {product.name}")

            else:

                print(f"❌ Product not found: {item['name']}")


        db.session.commit()

        print("\n🎉 All product images updated successfully")


if __name__ == "__main__":

    main()

# MyShop Django E-commerce Project

## Project Overview
MyShop is a Django-based e-commerce platform that allows users to browse products, manage their cart and wishlist, place orders, and read blog posts. The admin panel enables easy management of products, categories, orders, and blog content.

### Main Features
- Product catalog with categories, variations, images, and reviews
- Shopping cart and wishlist functionality
- Order placement and order history
- Discount codes
- Blog section for news and articles
- Admin dashboard for managing products, orders, and blog posts

## How to Run This Project

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- (Optional) Virtual environment tool (venv)

### Setup Steps
1. **Clone the repository**
   ```
   git clone <your-repo-url>
   cd store
   ```
2. **Create and activate a virtual environment (recommended)**
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
4. **Apply migrations**
   ```
   python manage.py migrate
   ```
5. **Create a superuser for admin access**
   ```
   python manage.py createsuperuser
   ```
6. **(Optional) Populate dummy data**
   ```
   python manage.py shell -c "import populate_dummy_data; populate_dummy_data.run()"
   ```
7. **Run the development server**
   ```
   python manage.py runserver
   ```
8. **Access the site**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure
- `shop/` - Product, order, wishlist, and discount code models and views
- `blog/` - Blog post models and views
- `core/` - Core site models (e.g., banners)
- `dashboard/` - Admin dashboard views
- `media/` - Uploaded images
- `static/` - Static files (CSS, JS, etc.)
- `templates/` - HTML templates
- `populate_dummy_data.py` - Script to generate sample products and blog posts

## Contact
For questions or support, contact: armughansaeed321@gmail.com

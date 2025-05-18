import random
from shop.models import Category, Product, Variation
from blog.models import BlogPost
from django.utils.text import slugify
from django.core.files import File
import os

# --- Dummy Categories ---
categories = [
    ('Clothing', 'clothing'),
    ('Electronics', 'electronics'),
    ('Books', 'books'),
]

# --- Dummy Variations ---
variations = [
    ('Standard', 'standard'),
    ('Limited Edition', 'limited-edition'),
    ('Bundle', 'bundle'),
]

# --- Dummy Sizes and Colors ---
sizes = ['S', 'M', 'L', 'XL']
colors = ['Red', 'Blue', 'Green', 'Black']

# --- Dummy Images ---
product_images = [
    'media/products/DSC_4985-scaled-1.webp',
]
blog_images = [
    'media/blog/screencapture-lukts-2025-03-17-00_12_25.png',
]

def get_image_file(image_list):
    path = random.choice(image_list)
    if os.path.exists(path):
        return File(open(path, 'rb'), name=os.path.basename(path))
    return None

# --- Dummy Products ---
def create_dummy_products():
    for cname, cslug in categories:
        cat, _ = Category.objects.get_or_create(name=cname, slug=cslug)
        for vname, vslug in variations:
            var, _ = Variation.objects.get_or_create(name=vname, slug=vslug)
            for size in sizes:
                for color in colors:
                    name = f"{cname} {vname} {size} {color}"
                    slug = slugify(f"{cname}-{vname}-{size}-{color}")
                    # Ensure unique slug for each product
                    if Product.objects.filter(slug=slug).exists():
                        continue
                    product = Product.objects.create(
                        name=name,
                        slug=slug,
                        category=cat,
                        size=size,
                        color=color,
                        price=random.randint(10, 200),
                        stock=random.randint(1, 50),
                        variation=var,
                        description=f"Dummy product: {name}",
                        is_featured=random.choice([True, False]),
                        show_on_homepage=random.choice([True, False]),
                        long_description=f"Long description for {name}.",
                        image_url="https://via.placeholder.com/300"
                    )
                    if not product.image:
                        img = get_image_file(product_images)
                        if img:
                            product.image.save(img.name, img, save=True)

def create_dummy_blogs():
    for i in range(1, 7):
        blog, created = BlogPost.objects.get_or_create(
            title=f"Dummy Blog Post {i}",
            slug=f"dummy-blog-post-{i}",
            content=f"This is the content for dummy blog post {i}.",
            is_featured=random.choice([True, False]),
            show_on_homepage=random.choice([True, False]),
        )
        if created and not blog.image:
            img = get_image_file(blog_images)
            if img:
                blog.image.save(img.name, img, save=True)

def run():
    create_dummy_products()
    create_dummy_blogs()
    print("Dummy products and blogs with images created.")

if __name__ == "__main__":
    run()

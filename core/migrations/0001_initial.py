# Generated by Django 5.2.1 on 2025-05-19 00:44

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AboutPageSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Image for the About page",
                        null=True,
                        upload_to="about/",
                    ),
                ),
                (
                    "title",
                    models.CharField(blank=True, default="About Us", max_length=200),
                ),
                (
                    "text",
                    models.TextField(
                        blank=True, default="We are passionate about what we do!"
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="HomeBanner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="banners/")),
                ("alt_text", models.CharField(blank=True, max_length=255)),
                (
                    "title",
                    models.CharField(
                        blank=True, default="Welcome to MyShop", max_length=200
                    ),
                ),
                (
                    "subtitle",
                    models.CharField(
                        blank=True,
                        default="Your one-stop shop for all your needs. Discover the latest products and deals!",
                        max_length=300,
                    ),
                ),
                (
                    "title_color",
                    models.CharField(
                        blank=True,
                        default="#ffffff",
                        help_text="Hex color for title text (e.g. #ffffff)",
                        max_length=20,
                    ),
                ),
                (
                    "subtitle_color",
                    models.CharField(
                        blank=True,
                        default="#ffffff",
                        help_text="Hex color for subtitle text (e.g. #ffffff)",
                        max_length=20,
                    ),
                ),
                (
                    "title_font",
                    models.CharField(
                        blank=True,
                        default="inherit",
                        help_text="CSS font-family for title (e.g. Montserrat, Arial)",
                        max_length=100,
                    ),
                ),
                (
                    "subtitle_font",
                    models.CharField(
                        blank=True,
                        default="inherit",
                        help_text="CSS font-family for subtitle (e.g. Roboto, Arial)",
                        max_length=100,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        help_text="Logo for navbar (recommended: square PNG)",
                        null=True,
                        upload_to="site/",
                    ),
                ),
                (
                    "navbar_text",
                    models.TextField(
                        blank=True,
                        default="MyShop",
                        help_text='HTML allowed. Example: Arm <span style="color:red">ughan</span>',
                    ),
                ),
                (
                    "navbar_text_color",
                    models.CharField(
                        blank=True,
                        default="#222",
                        help_text="Hex color for navbar text (e.g. #ff0000)",
                        max_length=20,
                    ),
                ),
                (
                    "navbar_text_font",
                    models.CharField(
                        blank=True,
                        default="inherit",
                        help_text="CSS font-family for navbar text (e.g. Montserrat, Arial)",
                        max_length=100,
                    ),
                ),
                (
                    "navbar_text_size",
                    models.CharField(
                        blank=True,
                        default="1.3rem",
                        help_text="CSS font-size for navbar text (e.g. 1.3rem, 20px)",
                        max_length=10,
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

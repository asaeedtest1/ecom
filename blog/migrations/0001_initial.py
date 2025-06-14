# Generated by Django 5.2.1 on 2025-05-19 00:44

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogPost",
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
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                ("content", models.TextField()),
                ("image", models.ImageField(blank=True, null=True, upload_to="blog/")),
                (
                    "image_url",
                    models.URLField(
                        blank=True,
                        help_text="Optional: Provide an image URL instead of uploading",
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "is_featured",
                    models.BooleanField(
                        default=False, help_text="Show as featured blog post"
                    ),
                ),
                (
                    "show_on_homepage",
                    models.BooleanField(
                        default=False, help_text="Show this blog post on homepage"
                    ),
                ),
            ],
        ),
    ]

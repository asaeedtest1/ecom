from django.db import models
from django.utils.text import slugify

# Create your models here.

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text='Optional: Provide an image URL instead of uploading')
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, help_text='Show as featured blog post')
    show_on_homepage = models.BooleanField(default=False, help_text='Show this blog post on homepage')

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return ''

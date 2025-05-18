from django.db import models
from django.contrib.auth.models import User

# Placeholder for static pages (no models needed for home/about/contact)

class HomeBanner(models.Model):
    image = models.ImageField(upload_to='banners/')
    alt_text = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=200, blank=True, default='Welcome to MyShop')
    subtitle = models.CharField(max_length=300, blank=True, default='Your one-stop shop for all your needs. Discover the latest products and deals!')
    title_color = models.CharField(max_length=20, blank=True, default='#ffffff', help_text='Hex color for title text (e.g. #ffffff)')
    subtitle_color = models.CharField(max_length=20, blank=True, default='#ffffff', help_text='Hex color for subtitle text (e.g. #ffffff)')
    title_font = models.CharField(max_length=100, blank=True, default='inherit', help_text='CSS font-family for title (e.g. Montserrat, Arial)')
    subtitle_font = models.CharField(max_length=100, blank=True, default='inherit', help_text='CSS font-family for subtitle (e.g. Roboto, Arial)')
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.alt_text or f"Banner {self.id}"

class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Logo for navbar (recommended: square PNG)')
    navbar_text = models.TextField(blank=True, default='MyShop', help_text='HTML allowed. Example: Arm <span style="color:red">ughan</span>')
    navbar_text_color = models.CharField(max_length=20, blank=True, default='#222', help_text='Hex color for navbar text (e.g. #ff0000)')
    navbar_text_font = models.CharField(max_length=100, blank=True, default='inherit', help_text='CSS font-family for navbar text (e.g. Montserrat, Arial)')
    navbar_text_size = models.CharField(max_length=10, blank=True, default='1.3rem', help_text='CSS font-size for navbar text (e.g. 1.3rem, 20px)')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Site Settings"

class AboutPageSettings(models.Model):
    image = models.ImageField(upload_to='about/', blank=True, null=True, help_text='Image for the About page')
    title = models.CharField(max_length=200, blank=True, default='About Us')
    text = models.TextField(blank=True, default='We are passionate about what we do!')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "About Page Settings"

from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone', 'loyalty_points')
    search_fields = ('user__username', 'address', 'phone')

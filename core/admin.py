from django.contrib import admin
from .models import HomeBanner, SiteSettings, AboutPageSettings

@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'alt_text', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('alt_text', 'title', 'subtitle')
    fieldsets = (
        (None, {
            'fields': ('image', 'alt_text', 'is_active')
        }),
        ('Banner Text', {
            'fields': ('title', 'title_color', 'title_font', 'subtitle', 'subtitle_color', 'subtitle_font')
        }),
    )

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("logo", "updated_at")
    fields = ("logo", "navbar_text", "navbar_text_color", "navbar_text_font", "navbar_text_size")
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists() or super().has_add_permission(request)

@admin.register(AboutPageSettings)
class AboutPageSettingsAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    fields = ("image", "title", "text")
    def has_add_permission(self, request):
        return not AboutPageSettings.objects.exists() or super().has_add_permission(request)

# Register your models here.

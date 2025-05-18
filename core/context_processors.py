from .models import SiteSettings, AboutPageSettings

def site_settings(request):
    return {
        'settings': SiteSettings.objects.first(),
        'about_page_settings': AboutPageSettings.objects.first(),
    }

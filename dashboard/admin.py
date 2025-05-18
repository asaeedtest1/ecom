from django.contrib import admin
from .models import VisitorLog

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'visit_date')
    search_fields = ('ip_address',)
    list_filter = ('visit_date',)

from django.contrib import admin
from .models import Category, Product, Order, OrderItem, DiscountCode, Wishlist, Variation, ProductImage, ProductReview
import csv
from django.http import HttpResponse

@admin.action(description="Export selected orders to CSV")
def export_orders_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=orders.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'User', 'Status', 'Created At'])
    for order in queryset:
        writer.writerow([order.id, order.user.username, order.status, order.created_at])
    return response

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_display = ("name", "slug")
    ordering = ("name",)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    search_fields = ("product__name", "user__username", "comment")
    list_filter = ("rating", "created_at")

admin.site.register(ProductReview, ProductReviewAdmin)

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ("user", "rating", "comment", "created_at")
    can_delete = True

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    list_display = ("name", "category", "price", "stock", "variation")
    list_filter = ("category", "variation")
    ordering = ("name",)
    fields = ("name", "slug", "category", "variation", "price", "stock", "image", "image_url", "size", "color", "is_featured", "show_on_homepage", "description", "long_description")
    inlines = [ProductImageInline, ProductReviewInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    actions = [export_orders_csv]
    inlines = []  # You can add OrderItemInline here if desired

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity")
    search_fields = ("order__id", "product__name")

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_value", "expiry_date")
    search_fields = ("code",)
    list_filter = ("expiry_date",)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "added_at")
    search_fields = ("user__username", "product__name")
    list_filter = ("added_at",)

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_display = ("name", "slug", "is_active")
    list_filter = ("is_active",)
    ordering = ("name",)

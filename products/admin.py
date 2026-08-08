from django.contrib import admin
from .models import Category, Product, BuyOffer

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'view_count', 'is_sold')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(BuyOffer)
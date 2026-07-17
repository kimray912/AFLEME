from django.contrib import admin
from .models import Profile
from products.models import Product
from django.db.models import Sum


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'get_name', 'student_id',
        'get_products_listed', 'get_sold_count', 'get_purchased_count',
        'get_total_views',
    )

    def get_name(self, obj):
        return obj.user.first_name
    get_name.short_description = '이름'

    def get_products_listed(self, obj):
        return Product.objects.filter(seller=obj.user).count()
    get_products_listed.short_description = '올린 상품 수'

    def get_sold_count(self, obj):
        return Product.objects.filter(seller=obj.user, is_sold=True).count()
    get_sold_count.short_description = '판매 완료'

    def get_purchased_count(self, obj):
        return Product.objects.filter(buyer=obj.user).count()
    get_purchased_count.short_description = '구매 수'

    def get_total_views(self, obj):
        total = Product.objects.filter(seller=obj.user).aggregate(Sum('view_count'))['view_count__sum']
        return total or 0
    get_total_views.short_description = '상품 총 조회수'


admin.site.register(Profile, ProfileAdmin)
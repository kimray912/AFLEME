from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('category/<str:category_name>/', views.category_view, name='category'),
    path('accounts/', include('accounts.urls')),
    path('sell/', views.sell_view, name='sell'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search_view, name='search'),
    path('notifications/', include('notifications.urls')),
    path('product/<int:product_id>/buy/', views.buy_view, name='buy_product'),
    path('product/<int:product_id>/edit/', views.edit_product_view, name='edit_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
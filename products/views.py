from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Product, Category
from notifications.models import Notification
from .forms import ProductForm


def home(request):
    products = Product.objects.all().order_by('is_sold', '-id')
    categories = Category.objects.all()

    recommended_products = None
    if request.user.is_authenticated:
        last_purchase = Product.objects.filter(buyer=request.user).order_by('-id').first()
        if last_purchase:
            recommended_products = Product.objects.filter(
                category=last_purchase.category,
                is_sold=False
            ).exclude(id=last_purchase.id)[:6]

    if request.user.is_authenticated:
        recent_notifications = Notification.objects.filter(user=request.user).order_by('-id')[:3]
        purchase_count = Product.objects.filter(buyer=request.user).count()
        sale_count = Product.objects.filter(seller=request.user, is_sold=True).count()
    else:
        recent_notifications = []
        purchase_count = 0
        sale_count = 0

    return render(request, 'products/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': None,
        'recent_notifications': recent_notifications,
        'purchase_count': purchase_count,
        'sale_count': sale_count,
        'recommended_products': recommended_products,
    })


def category_view(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category).order_by('is_sold', '-id')
    return render(request, 'products/category.html', {
        'category': category,
        'products': products,
    })


def search_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(title__icontains=query).order_by('is_sold', '-id') if query else Product.objects.none()
    categories = Category.objects.all()
    return render(request, 'products/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': None,
        'search_query': query,
    })


@login_required
def sell_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'products/sell.html', {'form': form})


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.view_count += 1
    product.save()

    if product.seller != request.user:
        request.user.profile.views_made += 1
        request.user.profile.save()

    return render(request, 'products/detail.html', {'product': product})


@login_required
def buy_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not product.is_sold and product.seller != request.user:
        product.is_sold = True
        product.buyer = request.user
        product.save()

        Notification.objects.create(
            user=request.user,
            product=product,
            message=f"'{product.title}' 상품 구매가 완료되었어요.",
            notification_type='trade',
        )
        Notification.objects.create(
            user=product.seller,
            product=product,
            message=f"'{product.title}' 상품이 판매되었어요.",
            notification_type='trade',
        )

        send_mail(
            subject='[AFLEME] 구매 완료 알림',
            message=f"'{product.title}' 상품 구매가 완료되었어요. (₩{product.price})",
            from_email=None,
            recipient_list=[request.user.email],
            fail_silently=True,
        )

    return redirect('product_detail', product_id=product.id)

@login_required
def edit_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.seller != request.user:
        return redirect('product_detail', product_id=product.id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit.html', {'form': form, 'product': product})

@login_required
def delete_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.seller != request.user and not request.user.is_staff:
        return redirect('product_detail', product_id=product.id)

    if request.method == 'POST':
        product.delete()
        return redirect('home')

    return redirect('product_detail', product_id=product.id)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category


def home(request):
    # Get all products and categories
    products = Product.objects.filter(available=True).select_related('category')
    categories = Category.objects.all()
    
    # Get selected category from query params
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'store/home.html', context)


def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, available=True).select_related('category')
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'current_category': category,
    }
    return render(request, 'store/home.html', context)


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    
    # Get related products from same category
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def about(request):
    """About us page"""
    return render(request, 'store/about.html')


def contact(request):
    """Contact us page"""
    return render(request, 'store/contact.html')


def quickview(request, product_slug):
    """Quick view for product (AJAX)"""
    product = get_object_or_404(Product, slug=product_slug, available=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'store/partials/quickview.html', {'product': product})
    
    # If not AJAX request, redirect to product detail
    return redirect('store:product_detail', product_slug=product_slug)


@login_required
@login_required
def wishlist(request):
    """User wishlist page"""
    from .models import Wishlist
    
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product', 'product__category')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'store/wishlist.html', context)

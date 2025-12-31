from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from decimal import Decimal


def get_cart(request):
    """Get cart from session or create new one"""
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    return cart


def save_cart(request, cart):
    """Save cart to session"""
    request.session['cart'] = cart
    request.session.modified = True


def add_to_cart(request, product_slug):
    """Add product to cart"""
    product = get_object_or_404(Product, slug=product_slug, available=True)
    cart = get_cart(request)
    
    product_id = str(product.id)
    
    if product_id in cart:
        # Update quantity if product already in cart
        cart[product_id]['quantity'] += int(request.POST.get('quantity', 1))
        messages.success(request, f'Updated {product.name} quantity in cart.')
    else:
        # Add new item to cart
        cart[product_id] = {
            'name': product.name,
            'slug': product.slug,
            'price': str(product.price),
            'quantity': int(request.POST.get('quantity', 1)),
            'image': product.image.url if product.image else None,
        }
        messages.success(request, f'Added {product.name} to cart.')
    
    save_cart(request, cart)
    return redirect('store:cart')


def cart(request):
    """View cart contents"""
    cart = get_cart(request)
    cart_items = []
    total_price = Decimal('0.00')
    
    for product_id, item in cart.items():
        # Get fresh product data for stock validation
        try:
            product = Product.objects.get(id=int(product_id))
            if product.available and product.stock > 0:
                # Calculate item total
                item_total = Decimal(item['price']) * item['quantity']
                total_price += item_total
                
                cart_items.append({
                    'id': product_id,
                    'product': product,
                    'name': item['name'],
                    'slug': item['slug'],
                    'price': Decimal(item['price']),
                    'quantity': item['quantity'],
                    'image': item['image'],
                    'item_total': item_total,
                    'available': product.available,
                    'stock': product.stock,
                })
        except Product.DoesNotExist:
            # Remove invalid items from cart
            del cart[product_id]
            save_cart(request, cart)
    
    # Calculate shipping threshold amount
    shipping_threshold = Decimal('50.00')
    shipping_needed = max(Decimal('0.00'), shipping_threshold - total_price)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': sum(item['quantity'] for item in cart_items),
        'shipping_needed': shipping_needed,
        'shipping_threshold': shipping_threshold,
    }
    return render(request, 'store/cart.html', context)


def update_cart(request, product_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart = get_cart(request)
        product_id = str(product_id)
        
        if product_id in cart:
            new_quantity = int(request.POST.get('quantity', 1))
            
            if new_quantity > 0:
                try:
                    product = Product.objects.get(id=int(product_id))
                    if new_quantity <= product.stock:
                        cart[product_id]['quantity'] = new_quantity
                        messages.success(request, 'Cart updated successfully.')
                    else:
                        messages.error(request, f'Only {product.stock} items available.')
                except Product.DoesNotExist:
                    messages.error(request, 'Product not found.')
            else:
                del cart[product_id]
                messages.success(request, 'Item removed from cart.')
            
            save_cart(request, cart)
    
    return redirect('store:cart')


def remove_from_cart(request, product_id):
    """Remove item from cart"""
    cart = get_cart(request)
    product_id = str(product_id)
    
    if product_id in cart:
        item_name = cart[product_id]['name']
        del cart[product_id]
        save_cart(request, cart)
        messages.success(request, f'Removed {item_name} from cart.')
    
    return redirect('store:cart')


def clear_cart(request):
    """Clear entire cart"""
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
        messages.success(request, 'Cart cleared successfully.')
    return redirect('store:cart')
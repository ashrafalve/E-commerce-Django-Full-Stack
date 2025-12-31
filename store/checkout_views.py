from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from decimal import Decimal
from .models import Order, OrderItem, Product
from .cart_views import get_cart, save_cart
import logging

logger = logging.getLogger(__name__)


def get_cart_items(request):
    """Get validated cart items with fresh product data"""
    cart = get_cart(request)
    cart_items = []
    
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            if product.available and product.stock > 0:
                cart_items.append({
                    'product': product,
                    'quantity': item['quantity'],
                    'price': item['price'],
                })
        except Product.DoesNotExist:
            logger.warning(f"Product {product_id} not found in cart")
    
    return cart_items


@login_required
def checkout(request):
    """Checkout page"""
    cart_items = get_cart_items(request)
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty. Add some products before checkout.')
        return redirect('store:cart')
    
    # Calculate total
    total_price = sum(Decimal(str(item['price'])) * item['quantity'] for item in cart_items)
    
    # Add shipping cost
    shipping_cost = Decimal('0.00') if total_price >= Decimal('50.00') else Decimal('5.99')
    final_total = total_price + shipping_cost
    
    if request.method == 'POST':
        try:
            print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
            print(f"DEBUG: User: {request.user}")
            
            # Check if user is still authenticated
            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in to place an order.')
                return redirect('login')
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                address=request.POST.get('address'),
                postal_code=request.POST.get('postal_code'),
                city=request.POST.get('city'),
                paid=False,
                status='pending'
            )
            
            print(f"DEBUG: Order created: {order.id}")
            
            # Create order items
            for item in cart_items:
                product = Product.objects.get(id=item['product'].id)
                
                if product.stock < item['quantity']:
                    order.delete()
                    raise ValidationError(f'Only {product.stock} items available for {product.name}')
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity']
                )
                
                product.stock -= item['quantity']
                product.save()
            
            # Clear cart
            request.session['cart'] = {}
            request.session.modified = True
            
            print(f"DEBUG: About to redirect to order confirmation for order {order.id}")
            messages.success(request, f'Order #{order.id} placed successfully!')
            return redirect('store:order_confirmation', order_id=order.id)
                
        except ValidationError as e:
            print(f"DEBUG: Validation error: {e}")
            messages.error(request, str(e))
        except Exception as e:
            print(f"DEBUG: Exception: {e}")
            logger.error(f"Checkout error: {e}")
            messages.error(request, 'An error occurred while processing your order. Please try again.')
    
    # Pre-fill form with user data if available
    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'first_name': request.user.first_name or '',
            'last_name': request.user.last_name or '',
            'email': request.user.email or '',
        }
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'final_total': final_total,
        'initial_data': initial_data,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.select_related('product')
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'store/order_confirmation.html', context)


@login_required
def order_history(request):
    """View order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'store/order_history.html', context)
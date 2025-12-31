from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Product, Wishlist
import logging

logger = logging.getLogger(__name__)


@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Check if product is in wishlist
        try:
            product = get_object_or_404(Product, id=product_id)
            in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
            
            return JsonResponse({
                'success': True,
                'in_wishlist': in_wishlist
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    elif request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            product = get_object_or_404(Product, id=product_id, available=True)
            
            # Check if already in wishlist
            try:
                wishlist_item = Wishlist.objects.get(user=request.user, product=product)
                # Item exists, remove it
                wishlist_item.delete()
                return JsonResponse({
                    'success': True,
                    'message': f'{product.name} removed from wishlist',
                    'action': 'removed'
                })
            except Wishlist.DoesNotExist:
                # Item doesn't exist, add it
                Wishlist.objects.create(user=request.user, product=product)
                return JsonResponse({
                    'success': True,
                    'message': f'{product.name} added to wishlist',
                    'action': 'added'
                })
                
        except Exception as e:
            logger.error(f"Error adding to wishlist: {e}")
            return JsonResponse({
                'success': False,
                'message': f'Error updating wishlist: {str(e)}'
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            product = get_object_or_404(Product, id=product_id)
            wishlist_item = Wishlist.objects.get(user=request.user, product=product)
            wishlist_item.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'{product.name} removed from wishlist'
            })
            
        except Wishlist.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Item not in wishlist'
            }, status=404)
        except Exception as e:
            logger.error(f"Error removing from wishlist: {e}")
            return JsonResponse({
                'success': False,
                'message': 'Error removing from wishlist'
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def share_product(request, product_slug):
    """Handle product sharing"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            product = get_object_or_404(Product, slug=product_slug)
            
            # Generate share URL
            share_url = request.build_absolute_uri(product.get_absolute_url())
            
            # Here you could implement:
            # - Email sharing
            # - Social media sharing
            # - Copy to clipboard
            
            return JsonResponse({
                'success': True,
                'message': 'Product link copied to clipboard!',
                'share_url': share_url,
                'product_name': product.name
            })
            
        except Exception as e:
            logger.error(f"Error sharing product: {e}")
            return JsonResponse({
                'success': False,
                'message': 'Error sharing product'
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
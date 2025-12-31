def cart_count(request):
    """Add cart count to all templates"""
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    
    cart_count = 0
    for item in cart.values():
        cart_count += item.get('quantity', 0)
    
    return {'cart_count': cart_count}
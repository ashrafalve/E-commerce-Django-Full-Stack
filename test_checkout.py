from django.contrib.auth.models import User
from store.models import Product, Order, OrderItem
from store.cart_views import get_cart, save_cart
from django.test import RequestFactory

def test_checkout():
    # Create test request
    factory = RequestFactory()
    request = factory.post('/checkout/')
    request.user = User.objects.get(username='testuser')
    request.session = {}

    # Add items to cart
    cart = {
        '1': {'name': 'Wireless Headphones', 'slug': 'wireless-headphones', 'price': '199.99', 'quantity': 1, 'image': None},
        '3': {'name': 'Cotton T-Shirt', 'slug': 'cotton-t-shirt', 'price': '29.99', 'quantity': 2, 'image': None}
    }
    save_cart(request, cart)

    # Check orders before checkout
    orders_before = Order.objects.count()
    print(f'Orders before checkout: {orders_before}')

    # Simulate checkout data
    request.POST = {
        'first_name': 'Test',
        'last_name': 'User', 
        'email': 'test@example.com',
        'address': '123 Test St',
        'city': 'Test City',
        'postal_code': '12345'
    }

    # Test checkout process
    from store.checkout_views import get_cart_items, checkout
    try:
        response = checkout(request)
        print('Checkout completed successfully!')
        
        # Check orders after checkout
        orders_after = Order.objects.count()
        print(f'Orders after checkout: {orders_after}')
        
        # Check created order
        order = Order.objects.latest('created_at')
        print(f'Order #{order.id} created for {order.first_name} {order.last_name}')
        print(f'Order status: {order.status}')
        print(f'Order items: {order.items.count()}')
        print(f'Order total: ${order.get_total_cost()}')
        
        # Check cart is cleared
        cart_after = get_cart(request)
        print(f'Cart items after checkout: {len(cart_after)}')
        
        # Check stock updates
        headphones = Product.objects.get(id=1)
        tshirt = Product.objects.get(id=3)
        print(f'Headphones stock: {headphones.stock}')
        print(f'T-shirt stock: {tshirt.stock}')
        
    except Exception as e:
        print(f'Checkout failed: {e}')

if __name__ == '__main__':
    test_checkout()
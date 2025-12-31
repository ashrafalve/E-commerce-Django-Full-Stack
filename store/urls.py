from django.urls import path
from . import views
from . import cart_views
from . import checkout_views
from . import auth_views
from . import wishlist_views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('quickview/<slug:product_slug>/', views.quickview, name='quickview'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('login/', auth_views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', auth_views.SignUpView.as_view(), name='signup'),
    path('profile/', auth_views.profile, name='profile'),
    path('cart/', cart_views.cart, name='cart'),
    path('cart/add/<slug:product_slug>/', cart_views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', cart_views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', cart_views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', cart_views.clear_cart, name='clear_cart'),
    path('checkout/', checkout_views.checkout, name='checkout'),
    path('order/<int:order_id>/confirmation/', checkout_views.order_confirmation, name='order_confirmation'),
    path('orders/', checkout_views.order_history, name='order_history'),
    path('wishlist/add/<int:product_id>/', wishlist_views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', wishlist_views.remove_from_wishlist, name='remove_from_wishlist'),
    path('share/<slug:product_slug>/', wishlist_views.share_product, name='share_product'),
]
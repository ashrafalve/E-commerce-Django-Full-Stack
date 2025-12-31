from django.contrib import admin
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'get_cost')
    fields = ('product', 'price', 'quantity', 'get_cost')
    
    def get_cost(self, obj):
        return obj.get_cost()
    get_cost.short_description = 'Total Cost'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'email', 
                   'status', 'paid', 'get_total_cost', 'created_at')
    list_filter = ('status', 'paid', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'id')
    readonly_fields = ('created_at', 'updated_at', 'get_total_cost')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'first_name', 'last_name', 'email')
        }),
        ('Shipping Address', {
            'fields': ('address', 'postal_code', 'city')
        }),
        ('Order Status', {
            'fields': ('status', 'paid', 'created_at', 'updated_at')
        }),
    )
    
    def get_total_cost(self, obj):
        return f"${obj.get_total_cost():.2f}"
    get_total_cost.short_description = 'Total Cost'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available', 
                   'created_at')
    list_filter = ('category', 'available', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'price', 'quantity', 'get_cost')
    list_filter = ('order__status', 'product__category')
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('get_cost',)
    
    def get_cost(self, obj):
        return f"${obj.get_cost():.2f}"
    get_cost.short_description = 'Total Cost'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'product')

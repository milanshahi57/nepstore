from django.contrib import admin
from .models import Product, ContactMessage, UserProfile, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'brand', 'created_at')
    search_fields = ('name', 'description', 'brand')
    list_filter = ('created_at', 'brand')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('submitted_at',)
    readonly_fields = ('name', 'email', 'message', 'submitted_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'phone', 'address')
    list_filter = ('created_at',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'total_amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_completed', 'created_at']
    search_fields = ['user__username', 'full_name', 'email', 'phone']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'full_name', 'email', 'phone')
        }),
        ('Shipping Information', {
            'fields': ('address', 'city', 'state', 'zip_code', 'order_notes')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'payment_method', 'payment_completed', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Add custom actions for updating order status
    actions = ['mark_as_pending', 'mark_as_delivering', 'mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_pending(self, request, queryset):
        queryset.update(status='pending')
        self.message_user(request, f"{queryset.count()} order(s) marked as pending.")
    mark_as_pending.short_description = "Mark selected orders as Pending"
    
    def mark_as_delivering(self, request, queryset):
        queryset.update(status='delivering')
        self.message_user(request, f"{queryset.count()} order(s) marked as delivering.")
    mark_as_delivering.short_description = "Mark selected orders as Delivering"
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
        self.message_user(request, f"{queryset.count()} order(s) marked as delivered.")
    mark_as_delivered.short_description = "Mark selected orders as Delivered"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} order(s) marked as cancelled.")
    mark_as_cancelled.short_description = "Mark selected orders as Cancelled"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'total')
    search_fields = ('order__id', 'product__name')



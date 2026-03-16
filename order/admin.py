from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'quantity', 'price', 'total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'created_at',
        'status',
        'shipping_name',
        'shipping_sity',
        'shipping_street',
        'total_price',
    )
    search_fields = ('user__username',)
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Основна інформація', {
            'fields': ('user', 'status'),
        }),
        ('Системна інформація', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )



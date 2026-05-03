from django.contrib import admin
from .models import Order, OrderItem

from django.urls import reverse
from django.utils.safestring import mark_safe

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def order_invoice(obj):
    url = reverse('orders:admin_order_invoice', args=[obj.id])
    return mark_safe(f'<a href="{url}" target="_blank" class="button" style="background-color: #8b0000; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px; font-weight: bold; white-space: nowrap; display: inline-block;">View Invoice</a>')

order_invoice.short_description = 'Invoice'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone_number',
                    'address', 'city', 'paid',
                    'created', order_invoice]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)
    mark_as_paid.short_description = "Mark selected orders as paid"

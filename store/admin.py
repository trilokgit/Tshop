from django.contrib import admin
from .models import Tshirt, Brand, Occasion, Color, Sleeve, NackType, IdealFor, SizeVariant, Cart, Payment, Order, OrderItem
from django.contrib.auth.models import User
from django.utils.html import format_html
# Register your models here.


class SizeVariantConfiguration(admin.TabularInline):
    model = SizeVariant


class OrderItemConfiguration(admin.TabularInline):
    model = OrderItem


class TshirtConfiguration(admin.ModelAdmin):
    inlines = [SizeVariantConfiguration]
    list_display = ['get_image', 'name', 'discount']
    list_editable = ['discount']
    list_display_links=["name"]
    list_per_page=5

    def get_image(self, obj):
        return format_html(f"""
         
         <a href="{obj.image.url}" target = "_blank"><img src="{obj.image.url}" height='50px' /></a>
        
        """)


class OrderConfiguration(admin.ModelAdmin):

    list_display = ['user', 'shipping_address', 'phone',
                    'date', 'order_status', 'payment_method']

    readonly_fields = ('user', 'phone', 'shipping_address', 'total',
                       'payment_method', 'payment', 'payment_request_id', 'payment_id', 'payment_status')

    fieldsets = (
        ("Order Infromation", {"fields": ('order_status',
         'shipping_address', 'phone', 'total', 'user')}),
        ("Payment Information", {
         "fields": ('payment', 'payment_request_id', 'payment_id', 'payment_status')})

    )

    inlines = [OrderItemConfiguration]

    def payment_request_id(self, obj):
        return obj.payment_set.all()[0].payment_request_id

    def payment_status(self, obj):
        return obj.payment_set.all()[0].payment_status

    def payment_id(self, obj):
        payment_id = obj.payment_set.all()[0].payment_id
        if(payment_id is None or payment_id == ''):
            return "Payment id is not Available"
        else:
            return payment_id

    def payment(self, obj):
        payment_id = obj.payment_set.all()[0].id
        return format_html(f'<a href="/admin/store/payment/{payment_id}/change/" target="_blank">Click for payment information</a>')


class CartConfiguration(admin.ModelAdmin):
    model = Cart

    list_display = ['id', 'quantity', 'size', 'tshirt', 'user', 'username']
    fieldsets = (

        ("Cart Info", {"fields": ('username', 'get_sizeVariant',
         'quantity', 'get_tshirt', 'email')}),
    )

    readonly_fields = ('quantity', 'username',
                       'get_sizeVariant', 'get_tshirt', 'email')

    def get_tshirt(self, obj):
        tshirt = obj.sizeVariant.tshirt
        tshirt_id = tshirt.id
        name = tshirt.description
        return format_html(f'<a href="/admin/store/tshirt/{tshirt_id}/change/" target="_blank">{name}</a>')

    def get_sizeVariant(self, obj):
        return obj.sizeVariant.size

    get_tshirt.short_description = 'Tshirt'
    get_sizeVariant.short_description = 'Size'

    def size(self, obj):
        return obj.sizeVariant.size

    def tshirt(self, obj):
        return obj.sizeVariant.tshirt.description

    def username(self, obj):
        return obj.user.first_name

    def email(self, obj):
        return obj.user.email


admin.site.register(Tshirt, TshirtConfiguration)
admin.site.register(Brand)
admin.site.register(Occasion)
admin.site.register(Color)
admin.site.register(Sleeve)
admin.site.register(NackType)
admin.site.register(IdealFor)
admin.site.register(Cart, CartConfiguration)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Order, OrderConfiguration)

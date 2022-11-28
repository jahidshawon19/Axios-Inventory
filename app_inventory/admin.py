from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    search_fields=['mobile', 'email']
    list_filter=['types']
    list_display = ['full_name', 'email', 'mobile', 'address']

admin.site.register(Vendor, VendorAdmin)


class UnitAdmin(admin.ModelAdmin):
    search_fields=['title']
    list_display=['title']

admin.site.register(Unit, UnitAdmin)



class CategoryAdmin(admin.ModelAdmin):
    search_fields=['category_name']
    list_display=['category_name']

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_filter=['category']
    search_fields=['product_name', 'category']
    list_display=['product_name', 'category', 'unit']
admin.site.register(Product, ProductAdmin)



class PurchaseAdmin(admin.ModelAdmin):
    search_fields=['product']
    list_filter=['vendor', 'product__category']
    list_display=['vendor', 'product', 'unit', 'quantity',  'price', 'total_amount', 'purchase_date']

admin.site.register(Purchase, PurchaseAdmin)



class SalesAdmin(admin.ModelAdmin):
    search_fields=['product']
    list_filter=['customer_name', 'customer_mobile']
    list_display=['customer_name','customer_mobile', 'product',  'unit','quantity', 'price', 'total_amount', 'sales_date']

admin.site.register(Sales, SalesAdmin)



class InventoryAdmin(admin.ModelAdmin):
    search_fields=['product__product_name']
    search_input_placeholder = 'Search Product Name'
    list_filter=['Purchase__vendor', 'sale__customer_name']
    
    list_display = [ 'product', 'product_unit', 'sales_quantity', 'purchase_quantity', 'total_quantity', 'pur_date', 'sale_date', 'customer', 'vendor']
admin.site.register(Inventory,InventoryAdmin)


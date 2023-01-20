from django.contrib import admin
from . import models # from .models import Products

# Register your models here.
admin.site.site_header = 'Tutorial website for OnlineShop' 
admin.site.site_title = 'OnlineShop'
admin.site.index_title = 'Manage OnlineShop'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)

    def set_price_to_zero(self, request, queryset):
        queryset.update(price=0)

    actions = ('set_price_to_zero',)  
    list_editable = ('price','description')

admin.site.register(models.Products, ProductAdmin)
admin.site.register(models.OrderDetail)
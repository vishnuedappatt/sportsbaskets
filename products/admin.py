from django.contrib import admin
from .models import Product, Reviews,Section,Brand,Cart,CartItem,Variation,Wishlist,DiscountCoupon,Discount




class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug':('name',)}
    list_display=('name','slug')


class variationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active') 


class CartAdmin(admin.ModelAdmin):
    list_display =('cart_id','date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active')


admin.site.register(Product,ProductAdmin)
admin.site.register(Section)
admin.site.register(Brand)
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Variation,variationAdmin)
admin.site.register(Wishlist)
admin.site.register(DiscountCoupon)
admin.site.register(Discount)
admin.site.register(Reviews)
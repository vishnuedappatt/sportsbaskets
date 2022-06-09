from django import views
from django.urls import path
from . import views




urlpatterns = [
  path('',views.home,name='home'),
  path('cat/',views.categories,name='category'),
  path('search/',views.search,name="search"),
  path('cart/',views.cart,name='cart'),  
  path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
  path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name='remove_cart'),
  path('remove_cartitem/<int:product_id>/<int:cart_item_id>/',views.remove_cartitem,name='remove_cartitem'),
  path('category/<slug:category_slug>/',views.categories,name='categorylist'),
  path('category/<slug:category_slug>/<slug:subcategory_slug>/',views.subcategories,name='subcategorylist'),  
  path('category/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
  path('cart/checkout/',views.checkout,name='checkout'),
]
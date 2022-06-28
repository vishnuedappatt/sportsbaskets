from django import views
from django.urls import path
from . import views




urlpatterns = [
  path('',views.AdminHome,name='adminhome'),
  path('search/',views.Paymentsearch,name="Paymentsearch"),
  path('customers/',views.customers,name='customers'),
  path('customers/search/',views.customersearch,name='customersearch'), 
  path('customer/<int:id>/',views.customersUnBlock,name='customersUnBlock'),
  # category
  path('category/',views.Categoryshow,name="Categoryshow"),
  path('category/search/',views.categorysearch,name="categorysearch"),
  path('category/add/',views.AddCategory,name='addCategory'),
  path('category_edit/<str:slug>/',views.EditCategory,name='EditCategory'),  
  path('category_delete/<str:slug>/',views.DeleteCategory,name='DeleteCategory'),
  # subcategory
  path('subcategory/',views.SubCategoryshow,name='SubCategoryshow'),
  path('subcategory/search/',views.subcategorysearch,name='subcategorysearch'),
  path('subcategory/<str:slug>/',views.EditSubCategory,name='EditSubCategory'),
  path('subcategory_delete/<str:slug>/',views.DeleteSubCategory,name='DeleteSubCategory'),
  path('subcat/add/',views.AddSubCategory,name='AddSubCategory'),
  # product
  path('products/',views.product_show,name='product_show'),
  path('products/search/',views.productsearch,name='productsearch'),
  path('products_delete/<str:slug>/',views.delete_pro,name='delete_pro'),
  path('products_edit/<str:slug>/',views.edit_product,name='edit_product'),
  path('products_add/',views.add_product,name='addproduct'),
  #dependend drop dwn
  path('ajax/load-subcategory/', views.load_subcategory, name='ajax_load_subcategory'),
  # section
  path('sections/',views.Section_show,name='Section_show'),
  path('sections/search/',views.sectionsearch,name='sectionsearch'),
  path('secction_add/',views.addsection,name='addsection'),
  path('section_edit/<int:id>/',views.editsection,name='editsection'),
  path('section_delete/<int:id>/',views.deletesection,name='deletesection'),
  # duscount
  path('discount/',views.discount_Show,name='discount_Show'),
  path('discount/add/',views.add_discount,name='add_discount'),
  path('discount/search/',views.searchdiscount,name='searchdiscount'),
  path('discount/<int:id>/',views.edit_discount,name='edit_discount'), 
  path('discount_delete/<int:id>/',views.delete_discount,name='delete_discount'),

  #order

  path('orders/',views.OrderProduct_show,name='OrderProduct_show'),
  path('orders/search/',views.searchorderproduct,name='searchorderproduct'),
  path('order/edit/<int:id>/',views.editstatus,name='editstatus'),
  path('chart/',views.charts,name='charts'),
  # path('pie-chart/', views.pie_chart, name='pie-chart'),
  path('chart/pop/', views.quantity_chart, name='quantity_chart'),
  path('chart/category/', views.category_chart, name='category_chart'),

  # variation
  path('variations/',views.variationsshow,name="variationshow"),
  path('variations/search/',views.searchvaraition,name="searchvaraition"),
  path('variations/add/',views.add_variation,name="add_variation"),
  path('variations/<int:id>/',views.edit_variation,name="edit_variation"),
  path('variation_delete/<int:id>/',views.delete_variation,name="delete_variation"),

#brand
  path('brand/',views.brandshow,name='brand'),
  path('brand_edit/<int:id>/',views.edit_brand,name='edit_brand'),
  path('brand_add/',views.add_brand,name='add_brand'),
  path('brand_delete/<int:id>/',views.delete_brand,name='delete_brand'),


  path('reviews/',views.reviews,name='review'),
  path('reviews/<int:id>/',views.delete_review,name='delete_review'),
  
  path('pdf/',views.paymentlist,name='paymentlist'),
  path('logout/',views.adminlogout,name="adminlogout"),
  path('login/',views.admin_login,name="admin_login"),
]
from django.contrib import admin
from . models import Category,SubCategory
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug':('title',)}
    list_display=('title','slug')

class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug':('name',)}
    list_display=('name','slug')


admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
     
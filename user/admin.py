from django.contrib import admin
from .models import Account,Address
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display =('email','first_name','last_name','username','last_login','date_jointed','is_active')
    list_filter=()
    filter_horizontal=()
    fieldsets=()




admin.site.register(Account,AccountAdmin)
admin.site.register(Address)

from django import views
from django.urls import path
from . import views



urlpatterns=[
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    # path('home',views.home,name="home"), 
    path('activate/<uidb64>/<token>',views.activate,name="activate"),
    path('forgot_password/',views.forgot_password,name="forgot_password"),
    path('resetpassword_validate/<uidb64>/<token>',views.resetpassword_validate,name="resetpassword_validate"),
    path('resetPassword/',views.resetPassword,name="resetPassword"), 
    path('verify/', views.verify_code,name='verify'),  

]          
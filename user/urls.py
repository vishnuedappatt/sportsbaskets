from django import views
from django.urls import path
from . import views



urlpatterns=[
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('not_verified/',views.not_verified,name='not_verified'),
    # path('home',views.home,name="home"), 
    path('activate/<uidb64>/<token>',views.activate,name="activate"),
    path('forgot_password/',views.forgot_password,name="forgot_password"),
    path('resetpassword_validate/<uidb64>/<token>',views.resetpassword_validate,name="resetpassword_validate"),
    path('resetPassword/',views.resetPassword,name="resetPassword"), 
    path('verify/', views.verify_code,name='verify'),
    path('profile/',views.profile,name="profile"),  
    path('profile/edit/<int:id>/',views.Pofile_edit,name='Pofile_edit'),
    path('profile/dashboard/',views.dashboard,name="dashboard"),
    path('profile/dashboard/invoice/<int:order_id>/',views.invoice,name="invoice"),
    path('profile/dashboard/change_password/',views.change_password,name="change_password"),
    path('profile/dashboard/<int:id>/',views.review,name="review"),
    path('contact/',views.contact,name='contact'),
    path('pdf/<int:order_id>/',views.invoicepdf,name='invoicepdf'),
  
    
    

]          
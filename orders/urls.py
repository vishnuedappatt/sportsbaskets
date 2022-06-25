from django import views
from django.urls import path
from . import views




urlpatterns = [
    path('place_order/',views.place_order,name="place_order"),
    path('payments/',views.payments,name='payments'),
    path('payments/cod/',views.cod,name='cod'),
    path('payments/cod/verify/',views.cod_verify,name='cod_verify'),
  
    
    path('payment_status/',views.payment_status,name='payment_status'),
    path('captcha_verify/',views.captcha_verify,name='captcha_verify'),

    # path('payment/refund/<int:id>/',views.refund_payment,name='refund_payment'),
]
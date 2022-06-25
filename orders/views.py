
from django.shortcuts import redirect, render

from products.models import CartItem
from products.models import Product
from products.models import Discount

from .models import Order, OrderProduct,Payment
import datetime
from user.models import Address
import razorpay
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from user.views import send,check
# Create your views here.
from user.urls import *

import json
import urllib

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages



def place_order(request,total=0,quantity=0):
    current_user=request.user
    cart_items= CartItem.objects.filter( user=current_user)
    cart_count=cart_items.count()
    print('heyyy')
    if cart_count <= 0:
       return redirect('home')

    grand_total=0
    tax=0    
    value=0
    discount=0
    grand_total_without=0
    for cart_item in  cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity +=cart_item.quantity
    
    tax =(2* total)/100
    grand_total_without=total+tax
    print('welcome')
    try:
        data=Discount.objects.get(user=request.user)
        discount=data.discount_appiled
        print('discount'+ str(discount))
        value=grand_total_without * discount
        print(value)
        grand_total=grand_total_without-value
    except:
        grand_total=total+tax
 
   
    if request.method =='POST': 
        if 'address' in request.POST:                     
            address=request.POST['address']      
            address=Address.objects.get(id=address) 
            print('address')
            data= Order()
            data.user=request.user                                
            data.address=address      
            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
        
            #generate order number
            yr= int(datetime.date.today().strftime('%Y'))
            dt= int(datetime.date.today().strftime('%d'))
            mt= int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date =d.strftime("%Y%m%d")
            
            order_number=current_date +str(data.id)
            print(order_number)
            request.session['order_number']=order_number
            data.order_number = order_number
            data.save()

            current_user=request.user
            hey=Order.objects.all()
            print('fdsgfg')
            print(hey)
            
            orders= Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)


            context={
                'order':orders,
                'tax':tax,
                'total':total,
                'cart_items':cart_items,
                'grand_total':grand_total,
                'address':address,   
                'grand_total_without':grand_total_without,
                'discount_available':discount,
                
            }
            return render(request,'orders/payments.html',context)
        else:
            messages.error(request,'please enter a address for continue purpose')
            return redirect('checkout')
        
    else: 
        return redirect('checkout')

 


def payments(request):
    current_user=request.user
    cart_items= CartItem.objects.filter( user=current_user)  
    
    grand_total=0
    tax=0
    quantity=0
    total=0
    for cart_item in  cart_items:
        total += (cart_item.product.price *cart_item.quantity)
        quantity +=cart_item.quantity
    tax =(2* total)/100
    totale=total
    grand_total_without =int(total+tax)*100
    try: 
        data=Discount.objects.get(user=request.user)
        discount=data.discount_appiled     
        value=grand_total_without * discount
        print(value)
        grand_total=int(grand_total_without-value)
        data=Discount.objects.get(user=request.user)
        data.delete()
    except:
        grand_total=int(total+tax)*100

    paisa=grand_total/100
   
   
    #razorpay

    Client=razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_KEY))
    #creating order
    response_payment=Client.order.create(dict(amount=grand_total,currency='INR'))
    print(response_payment)
    order_id=response_payment['id']
    order_status=response_payment['status']
    total += (cart_item.product.price * cart_item.quantity)
    if order_status =='created':
        pay=Payment()
        pay.user=current_user
        pay.amount_paid=grand_total/100
        pay.order_id=order_id
        pay.save()
    
    context={
            'payment':response_payment,
            'grand_total':paisa,
            'tax':tax,   
            'total': totale,
        }
    return render(request,'orders/razor_payments.html',context)


def captcha_verify(request):
     if request.method=='POST':
        if 'g-recaptcha-response' in request.POST:
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                return redirect('payment_status')
            else:
                messages.error(request,'captcha error')



def payment_status(request):
    response=request.POST
    params_dict={ 
        'razorpay_order_id':response['razorpay_order_id'] ,
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],
        }
    
    client=razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_KEY))

    try:
        status=client.utility.verify_payment_signature(params_dict)
        payment=Payment.objects.get(order_id=response['razorpay_order_id'])
        payment.payment_id=response['razorpay_payment_id']
        payment.paid=True
        payment.save()

        
        order_number=request.session['order_number']
        print(order_number)
        order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
        order.payment=payment 
        order.status='Confirmed'
        order.save()
        
        cart_items=CartItem.objects.filter(user=request.user)
       
        print('firstt')
        for item in cart_items: 
            data=OrderProduct()
            print('uuuuu')
            data.order_id=order.id
            data.product_id=item.product_id
            data.user_id=request.user.id
            data.payment=payment
            print('kkkkkkkk')
            data.quantity=item.quantity
            data.product_price=item.product.price           
            data.ordered=True
            print('pppppp')
            data.method='Razorpay'
            data.save()



            print('secontt')  
            model=item.product
            print('loopp')           
            

            product=Product.objects.get(id=model.id)
            print('weksicnbjk')
            print(product)
            product.stock-= item.quantity
            product.save()  


        cart_items.delete()
       
        mail_subject ='Thankyou for ordering with Us'
        message= render_to_string('orders/order.html',{

            'user':request.user,
           'order_number':order_number,
        

                 })
        to_email = request.user.email
        send_email=EmailMessage(mail_subject, message ,to=[to_email])
        print("here")
        send_email.send()     

        return render(request,'orders/payment_status.html',{'status':True})
    except: 
        payment=Payment.objects.get(order_id=response['razorpay_order_id'])
        payment.payment_id=response['razorpay_payment_id']
        payment.paid=False
        payment.save()


        order_number=request.session['order_number']
        print(order_number)
        order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
        order.payment=payment 
        order.status='Failed'
        order.save()
        
        cart_items=CartItem.objects.filter(user=request.user)
        print('firstt')
        for item in cart_items: 
            data=OrderProduct()      
            data.order_id=order.id
            data.product_id=item.product_id
            data.user_id=request.user.id
            data.payment=payment         
            data.quantity=item.quantity
            data.product_price=item.product.price     
            data.ordered=False         
            data.save()
        return render(request,'orders/payment_status.html',{'status':False})



# def refund_payment(request,id):
#     order=OrderProduct.objects.get(id=id)
#     payment=order.payment
#     price=int(order.product_price)
#     print(payment)
#     print(price)
   


#     client = razorpay.Client(auth=("rzp_test_EsWN1MNLnJr3lq", "3mB15mFeOmloSZAV5j6UPjtm"))
#     client.payment.refund(payment,{
#     "amount": "100",
#     "speed": "normal",
#     "notes": {
#         "notes_key_1": "Beam me up Scotty.",
#         "notes_key_2": "Engage"
#     },
#     "receipt": "Receipt No. 31"
#     })

 
#     print('jkdshnkdjshnnjlnlkjj')
#     client.payment.fetch_multiple_refund(payment) 
#     print(payment)
#     data=Order()
#     data.status='Cancelled'
#     data.save()
#     return render('dashboard')

   
def cod(request):
    current_user=request.user
    cart_items= CartItem.objects.filter( user=current_user)  
    
    grand_total=0
    tax=0
    quantity=0
    total=0
    for cart_item in  cart_items:
        total += (cart_item.product.price *cart_item.quantity)
        quantity +=cart_item.quantity
    tax =(2* total)/100
    totale=total
    grand_total_without =int(total+tax)*100
    try: 
        data=Discount.objects.get(user=request.user)
        discount=data.discount_appiled     
        value=grand_total_without * discount
        print(value)
        grand_total=int(grand_total_without-value)
        data=Discount.objects.get(user=request.user)
        data.delete()
    except:
        grand_total=int(total+tax)*100

    paisa=grand_total/100

    if request.method=='POST':
        if 'g-recaptcha-response' in request.POST:
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                mobile=request.POST['mobile']
                request.session['captcha']=mobile
                send(mobile)  
                return redirect ('cod_verify')
                
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        else:
            messages.error(request,'Please verify captcha!!')
            return redirect('cod')
  
    order_number=request.session['order_number']
    pay=Payment()
    pay.user=current_user
    pay.amount_paid=paisa
    pay.order_id=order_number
    pay.save()

    context={
            # 'payment':response_payment,
            'grand_total':paisa,
            'tax':tax,   
            'total': totale,
        }
   
    return render(request,'orders/cod.html',context)






def cod_verify(request):
    if request.method == 'POST':
        code=request.POST['cod_code']
        mobile=request.session['captcha']
        order_number=request.session['order_number']
        if check(mobile,code):
            order_number=request.session['order_number']
            print(order_number)
            order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
         
            order.status='Confirmed'
            order.save()
            
            cart_items=CartItem.objects.filter(user=request.user)
            
            print('firstt')
            for item in cart_items: 
                data=OrderProduct()
                print('uuuuu')
                data.order_id=order.id
                data.product_id=item.product_id
                data.user_id=request.user.id                
                print('kkkkkkkk')
                data.quantity=item.quantity
                data.product_price=item.product.price           
                data.ordered=True
                data.method='COD'
                print('pppppp')
                data.save()



                print('secontt')  
                model=item.product
                print('loopp')           
                

                product=Product.objects.get(id=model.id)
                print('weksicnbjk')
                print(product)
                product.stock-= item.quantity
                product.save()  


            cart_items.delete()
            
            mail_subject ='Thankyou for ordering with Us'
            message= render_to_string('orders/order.html',{

                'user':request.user,
                'order_number':order_number,
            

                        })
            to_email = request.user.email
            send_email=EmailMessage(mail_subject, message ,to=[to_email])
            print("here")
            send_email.send()     
            messages.success(request,'your order placed success fullyy')
            return redirect('home')
        else:   
            return HttpResponse('failed')    
            
    return render(request,'orders/cod_verify.html')
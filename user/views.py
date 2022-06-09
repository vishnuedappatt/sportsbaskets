from ast import Sub
from email import message
from multiprocessing import context
import re
import site
# from typing_extensions import Required
import django
from django.http import HttpResponse
from django.shortcuts import redirect, render

# from sportsbasket import user

# from sportsbasket.products.models import Section

# from sportsbasket import user
# from sportsbasket import user
# from sportsbasket.user.models import Account
from .forms import RegistrationForm ,VerifyForm
from .models import Account
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


#products details

from products.models import Product
from category.models import Category,SubCategory

# otp verify
from products import urls
from .verify import send,check

#logined user cart
from products.models import *
from products.views import _cart_id

import requests


#for email verification


# def register(request):
#     if request.method == 'POST':
#         form =RegistrationForm(request.POST)
#         if form.is_valid():
#             first_name =form.cleaned_data['first_name']
#             last_name =form.cleaned_data['last_name']
#             phone_number =form.cleaned_data['phone_number']            
#             email =form.cleaned_data['email']
#             password =form.cleaned_data['password']
#             username=email.split("@")[0]
#             print('heyy')
#             user =Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
#             user.phone_number=phone_number
#             user.save()

#             current_site = get_current_site(request)
#             mail_subject ='please Activate your account'
#             message= render_to_string('user/user_verification.html',{
#                 'user':user,
#                 'domain': current_site,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':default_token_generator.make_token(user),
#                     })

#             to_email = email
#             send_email=EmailMessage(mail_subject, message ,to=[to_email])
#             print("here")
#             send_email.send()
#             print("herewego")
#             messages.success(request,'Registration successful')
#             return redirect('/user/login/?command=verification&email='+email)
            
#     else:        
#         form=RegistrationForm()
#     context={
#             'form':form
#             }
#     return render (request,'user/register.html',context)



def login(request):
    if request.method =='POST':
        email =request.POST['email']
        password=request.POST['Password']
        user=auth.authenticate(email=email,password=password)
        print('done')
        if user is not None:
            try:
                print('goooooggg')
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists= CartItem.objects.filter(cart=cart).exists()
                print(is_cart_item_exists)
                if is_cart_item_exists:
                    print('112222')
                    cart_item =CartItem.objects.filter(cart=cart)
                    product_variation=[]
                    for item in cart_item:
                        variation=item.variations.all()
                        product_variation.append(list(variation))


                    cart_item =CartItem.objects.filter(user=user)
                    ex_var_list=[]
                    id=[]
                    for item in cart_item:
                        existing_variation =item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)


                    for pr in product_variation:
                        if pr in ex_var_list:
                            index=ex_var_list.index(pr)
                            item_id=id[index]
                            item =CartItem.objects.get(id=item_id)
                            item.quantity +=1
                            item.user=user
                            item.save()
                        
                        else:
                            cart_item=CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()
                    

                  
            except:
                print('hhhhh')
                pass

            auth.login (request,user)          
            messages.success(request,'you are logined successfully')
            url=request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print(query)
                params =dict(x.split('=')for x in query.split('&'))
                print(params)
                if 'next' in params:
                    nextPage=params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')
        else:
             messages.error(request,'invalid cridential')
             return redirect('login')

    else: 
        context={ }
        return render (request,'user/login.html',context)
        
  

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request,'susessfully loged out')
    return redirect('login')


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user =Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        messages.success(request,'congradulation your account is activated')
        return redirect('login')
    else:
        messages.error(request,'invalid activation link')
        return redirect('register')        


# def home(request): 
#     Cat=Category.objects.all()
#     Sub=SubCategory.objects.all()
#     product=Product.objects.filter(section__name="main")
#     context={
    
#      'product':product,
#      'Cat':Cat,
#      'Sub':Sub,
       
#     }
#     return render(request,'products/home.html',context)


def forgot_password(request):
    if request.method =='POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject ='Reset password'
            message= render_to_string('user/forgot_password_email.html',{
                'user':user,
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

                    })
            to_email = email
            send_email=EmailMessage(mail_subject, message ,to=[to_email])
            print("here")
            send_email.send()
            print("herewego")
            messages.success(request,'Reset mail is sented your account')
            return redirect('login')

        else:
            messages.error(request,'entered email is not valid please enter currect one')
            return redirect('forgot_password')

    return render(request,'user/forgot_password.html')


def resetpassword_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user =Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
      user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link is expired!')
        return redirect('login')

    



def resetPassword(request):
    if request.method =='POST':
        password =request.POST['password']
        confirm_password =request.POST['confirm_password']


        if password == confirm_password:
            uid =request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password reset successsfully')
            return redirect('login')

        else:
            messages.error(request,'password do not match')
            return redirect('resetPassword')
    else:
        return render(request,'user/resetPassword.html')



def register(request):
    if request.method == 'POST':
        form =RegistrationForm(request.POST)
        if form.is_valid():
            first_name =form.cleaned_data['first_name']
            last_name =form.cleaned_data['last_name']
            phone_number =form.cleaned_data['phone_number']            
            email =form.cleaned_data['email']
            password =form.cleaned_data['password']
            username=email.split("@")[0]
            print('heyy')
            if Account.objects.filter(phone_number=phone_number).exists():
                messages.error(request,'phone number already exist')
            elif Account.objects.filter(email=email).exists():
                messages.error(request,'email  already exist')
            else:                       
                user =Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)            
                user.phone_number=phone_number
                user.save()
                request.session['phone_number']=phone_number
                send(form.cleaned_data.get('phone_number'))   
                messages.success(request,'OTP sent your phone number')              
                return redirect('verify')       
                                
               
              
            
    else:        
        form=RegistrationForm()
    context={
            'form':form,
            }
    return render (request,'user/register.html',context)


def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            print(code)
            print('x')   
            phone_number=request.session['phone_number']
            if check(phone_number, code):  
                user=Account.objects.get(phone_number=phone_number)
                user.is_active = True
                user.save()               
                return redirect('login')
    
    else:
        form = VerifyForm()
    return render(request, 'user/verify.html', {'form': form})

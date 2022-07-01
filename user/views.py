



from django.shortcuts import redirect, render

from products.forms import ReviewForm


from .forms import RegistrationForm ,VerifyForm,EditProfileForm
from .models import Account,Address
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

from products.models import Reviews

from adminz.models import BlockedUser

from orders.models import OrderProduct,Order

# otp verify

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
        account=Account.objects.filter(email=email,is_active=False).exists()
     
        print('heyy')
        if account :
            account_user=Account.objects.get(email=email,is_active=False)   
            print(account_user)    
            mobile=account_user.phone_number
            block=BlockedUser.objects.filter(phone=mobile).exists()
            if not block:
                send(mobile)                 
                messages.success(request,'OTP sent your phone number')              
                return redirect('verify')     
            else:
                messages.error(request,'you are blocked from here sorry')
        
        user=auth.authenticate(email=email,password=password)
        print('done')
        if user is not None:
            if user.is_superadmin: 
                messages.error(request,'No entry')                    
                return redirect('login')
            else:         
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
             messages.error(request,'invalid credential')
             return redirect('login')

    else: 
        context={ }
        return render (request,'user/login.html',context)
        
  

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request,'successfully loged out')
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
        print('adfdfafdd')
        if form.is_valid():
            first_name =form.cleaned_data['first_name']
            last_name =form.cleaned_data['last_name']
            phone_number =form.cleaned_data['phone_number']            
            email =form.cleaned_data['email']
            password =form.cleaned_data['password']
            username=email.split("@")[0]
            length=len(password)
            print('heyy')
            print('helloooeerr')
            if Account.objects.filter(phone_number=phone_number).exists():
                messages.error(request,'phone number already exist')
                
                
            elif Account.objects.filter(email=email).exists():
                messages.error(request,'email  already exist')
               
            elif length <8:
                messages.error(request,'password should be 8 strong charectors')
               
            else:                       
                user =Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)            
                user.phone_number=phone_number
                user.save()
                request.session['phone_number']=phone_number
                print(phone_number)
                send(form.cleaned_data.get('phone_number'))  
                print(phone_number) 
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




@login_required(login_url='login')
def profile(request):
    user=request.user
    print(user)
    users=Account.objects.get(email=user)
    account=Address.objects.filter(user=user)[0:1]
    print(users)
    return render(request,'user/profile.html',{'user':users,'account':account})
    



@login_required(login_url='login')
def Pofile_edit(request,id):
    try:
         
        account=Account.objects.get(id=id)
        form=EditProfileForm(instance=account)
        print(form.is_valid()) 
        if request.method== 'POST':
            print('catcck')
            form=EditProfileForm(request.POST,instance=account)
            print(form.is_valid)
            if form.is_valid():
                print('jakdkdkjd')
                form.save()         
                return redirect('profile')
            else:
                print("huuhu")

        context={
            'form':form,
        }
        return render(request,'user/update.html',context)
    except:
        messages.error(request,'you are doing something wrongg!!')
        return redirect('profile')



@login_required(login_url='login')
def dashboard(request):
    item=OrderProduct.objects.filter(user=request.user)
    
    context={
        'item':item,
    }
    return render (request,'user/dashboard.html',context)





def not_verified(request):
    if request.method=='POST':
        phone_number=request.POST['phone_number']
        request.session['phone_number']=phone_number
        acc=Account.objects.filter(phone_number=phone_number,is_active=False).exists()        
        block=BlockedUser.objects.filter(phone=phone_number).exists()
       
        if acc:
            if not block:
                send(phone_number) 
                return redirect('verify')
            else:
                messages.error(request,'you have been blocked')
                return redirect('login')

        else:
            messages.error(request,'you are not a member')
            return redirect('login')

    else:
        return render(request,'user/not_verified.html')



     

def change_password(request):
    if request.method=='POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']

        user=Account.objects.get(email=request.user.email)

        if new_password==confirm_password:            
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'successfully change the password')
                return redirect('login')
            else:
                messages.error(request,'incorrect current password')
                return redirect('change_password')
        else:
            messages.error(request,'password missmatch')
    else:
        return render(request,'user/change_password.html')








def review(request,id):
    pro=OrderProduct.objects.get(id=id)
    product=pro.product
    print(product)
    member=request.user
    form=ReviewForm()   
    rating=None
    if request.method=='POST':
        value=request.POST['description']            
        images=request.FILES['image']
        if 'star' in request.POST:
            rating=request.POST['star']
   
        print(value)
        print(images)
        print(member)
        data=Reviews()
        data.user=member
        data.product=product
        data.image=images
        data.description=value
        data.rating=rating
        data.save()      
        messages.success(request,'Review added successfully')
        print(';dsdd')
        return redirect('dashboard')

    context={'form':form,}
    return render(request,'user/review.html',context)
        


def contact(request):
    return render(request,'user/contact.html')



def invoice(request,order_id): 
    order=Order.objects.get(id=order_id)   
    product=OrderProduct.objects.filter(order= order )

   
    print(order)
    return render(request,'user/invoice.html',{'order':order,'product':product,})



from adminz.utils import render_to_pdf

    
def invoicepdf(request,order_id):
    order=Order.objects.get(id=order_id)   
    product=OrderProduct.objects.filter(order= order )   

    template_name = "user/invoice.html"
   

    return render_to_pdf(
        template_name,
        {
       'order':order,
       'product':product,

        },
    )



from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from products.models import CartItem,Cart
from .models import Order
import datetime
from user.models import Address


# Create your views here.

def payments(request):
    return render(request,'orders/payments.html')





def place_order(request,total=0,quantity=0):
    current_user=request.user
    cart_items= CartItem.objects.filter( user=current_user)
    cart_count=cart_items.count()
    print('heyyy')
    if cart_count <= 0:
       return redirect('home')

    grand_total=0
    tax=0
    for cart_item in  cart_items:
        total =+ (cart_item.product.price *cart_item.quantity)
        quantity +=cart_item.quantity
    tax =(2* total)/100
    grand_total=total+tax
    print('welcome')
    if request.method =='POST':
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
            'cart_items':cart_items,
            'grand_total':grand_total,
            'address':address,
            
            
        }
        return render(request,'orders/payments.html',context)
        
    else:
        return redirect('checkout')



   
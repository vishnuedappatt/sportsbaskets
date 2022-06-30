
from django.shortcuts import redirect, render

from orders.models import OrderProduct,Order
from products.models import Product
from category.models import Category,SubCategory
from products.models import Section,Variation
from orders.models import Payment
from products.models import DiscountCoupon,Reviews
from products.models import Brand
from user.models import Account
from django.db.models import  Q
from .models import BlockedUser

from .forms import CategoryForm, DiscountForm,SubCategoryForm,ProductForm,SectionForm,OrderStatusform,VariationForm,BrandForm
from django.contrib import messages,auth

from django.contrib.auth.decorators import user_passes_test

from products.urls import *

from django.db.models import Sum
from django.http import JsonResponse



# Create your views here.

def admin_login(request):
    if request.method =='POST':
        email =request.POST['email']
        password=request.POST['Password'] 
        user=auth.authenticate(email=email,password=password)
        print('done')
        if user is not None:
            if user.is_superadmin:
                auth.login (request,user)
                request.session['admin']=password       
                return redirect('adminhome')
            else:
                messages.error(request,'No entry')
        else:
            messages.error(request,'invalid credentials')
    return render(request,'user/admin.html')



from django.contrib.auth.decorators import user_passes_test
account=Account.objects.filter(is_superadmin=True)
@user_passes_test(lambda u: u in account ,login_url='admin_login')



def AdminHome(request):
    account=Account.objects.filter( is_superadmin=False).count()
    payment=OrderProduct.objects.filter(ordered=True).count()    
    number=OrderProduct.objects.filter(ordered=True)
    transations=Payment.objects.all()    
    user=request.user
    sum=0
    
    # products=Product.objects.get(slug='nivia-supreme')
    for x in number:
        sum+=x.product_price

    pro_count=Product.objects.all().count()


    context={
        'account':account,
        'payment':payment,
        'sum':sum,
        'pro_count':pro_count,
        'transations':transations,
        'user':user,
        # 'pts':products,
               
    }
    return render(request,'adminz/homee.html',context)


def Paymentsearch(request):
    transations=0 
    if 'keyword' in request.GET:
        
        print('difuhdsiufhdufh')
        keyword=request.GET['keyword']   
        print(keyword)   
        if keyword:
            transations =Payment.objects.filter(Q(user__email__icontains=keyword)|Q(payment_id__icontains=keyword))
            context={
                'transations':transations,
      
            }
            return render(request,'adminz/homee.html',context)
            
        else:           
            return redirect('adminhome')
    context={
                'transations':transations,
      
            }
            
      
    return render(request,'adminz/homee.html',context)



@user_passes_test(lambda u: u in account ,login_url='admin_login')
def customers(request):
    account=Account.objects.filter( is_superadmin=False).order_by('-id')
    context={
        'account':account,
    }
    return render(request,'adminz/customers.html',context)



@user_passes_test(lambda u: u in account ,login_url='admin_login')
def customersearch(request):  
    if 'keyword' in request.GET:        
        print('difuhdsiufhdufh')
        keyword=request.GET['keyword']   
        print(keyword)   
        if keyword:
            account =Account.objects.filter(Q(email__icontains=keyword)|Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword)|Q(phone_number__icontains=keyword))
            context={
                'account':account,
      
            }
            return render(request,'adminz/customers.html',context)
            
        else:         
            return redirect('customers')
    



@user_passes_test(lambda u: u in account ,login_url='admin_login')
def customersUnBlock(request,id):    
    account=Account.objects.get(id=id)
    print(account)
    if  account.is_active:
        account.is_active=False
        account.save()
        print('blockedddd')
        block=BlockedUser()
        print('niiodoao')
        block.phone=account.phone_number
        block.save()
        print('daveddddddd')
      
    else:
        account.is_active=True
        account.save()
        num=account.phone_number
        print(num)
        block=BlockedUser.objects.get(phone=num)
        block.delete()
        print('deeletreeeee')
        
        # block.save()
        print('unnnnnnnblockedddd')

    return redirect('customers')




@user_passes_test(lambda u: u in account ,login_url='admin_login')
def Categoryshow(request):
    Cat=Category.objects.all().order_by('-id')

    context={
        'cat':Cat,
    }
    return render(request,'adminz/Category.html',context)




@user_passes_test(lambda u: u in account ,login_url='admin_login')
def categorysearch(request):
    try:  
        if 'keyword' in request.GET:        
            print('difuhdsiufhdufh')
            keyword=request.GET['keyword']   
            print(keyword)   
            if keyword:
                cat =Category.objects.filter(Q(title__icontains=keyword))
                context={
                    'cat':cat,
        
                }
                return render(request,'adminz/Category.html',context)
                
            else:
               
                return redirect('SubCategoryshow')
    except:
            messages.success(request,'no items found')
            return redirect('SubCategoryshow')


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def EditCategory(request,slug):
    cat=Category.objects.get(slug=slug)    
    form=CategoryForm(instance=cat)
    try:
        if request.method=='POST':
            form=CategoryForm(request.POST  ,request.FILES,instance=cat)
            if form.is_valid():
                form.save()
                return redirect('Categoryshow')
    except:
        messages.error(request,'exsisting slug')
        return redirect('EditCategory')

    context={
        'form':form,
    }
    return render(request,'adminz/Category_edit.html',context)


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def AddCategory(request):
    form=CategoryForm()
    try:
        if request.method=='POST':
            form=CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('Categoryshow')
    except:
            messages.error(request,'exsisting slug')
            return redirect('EditCategory')

    context={
        'form':form,
    }
    return render(request,'adminz/add_cateegory.html',context)

@user_passes_test(lambda u: u in account ,login_url='admin_login')
def DeleteCategory(request,slug):
    cat=Category.objects.get(slug=slug)
    cat.delete()
    return redirect('Categoryshow')


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def SubCategoryshow(request):
    sub=SubCategory.objects.all().order_by('-id')

    context={
        'cat':sub,
    }
    return render(request,'adminz/subcategory.html',context)




@user_passes_test(lambda u: u in account ,login_url='admin_login')
def subcategorysearch(request):
    try:  
        if 'keyword' in request.GET:        
            print('difuhdsiufhdufh')
            keyword=request.GET['keyword']   
            print(keyword)   
            if keyword:
                cat =SubCategory.objects.filter(Q(category__title__icontains=keyword)|Q(name__icontains=keyword))
                context={
                    'cat':cat,
        
                }
                return render(request,'adminz/subcategory.html',context)
                
            else:
               
                return redirect('Categoryshow')
    except:
            messages.success(request,'no items found')
            return redirect('Categoryshow')


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def EditSubCategory(request,slug):
    cat=SubCategory.objects.get(slug=slug)    
    form=SubCategoryForm(instance=cat)
    if request.method=='POST':
        form=SubCategoryForm(request.POST ,request.FILES,instance=cat)
        if form.is_valid():
            form.save()
            return redirect('SubCategoryshow')

    context={
        'form':form,
    }
    return render(request,'adminz/subcategory_edit.html',context)


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def AddSubCategory(request):
    form=SubCategoryForm()
    try:
        if request.method=='POST':
            form=SubCategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('SubCategoryshow')

    except:
        messages.error(request,'exsisting slug')
        return redirect('EditSubCategory')

    context={
        'form':form,
    }
    return render(request,'adminz/add_subcategory.html',context)



@user_passes_test(lambda u: u in account ,login_url='admin_login')
def DeleteSubCategory(request,slug):
    cat=SubCategory.objects.get(slug=slug)
    cat.delete()
    return redirect('SubCategoryshow')



@user_passes_test(lambda u: u in account ,login_url='admin_login')

def product_show(request):
    products=Product.objects.all().order_by('-id')

    context={
        'products':products,
    }
    return render(request,'adminz/pro_show.html',context)


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def productsearch(request): 
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        print('hey')
        if keyword:
            products =Product.objects.order_by('-id').filter(Q(name__icontains=keyword) | Q(category__title__icontains=keyword) | Q(brand__name__icontains=keyword) | Q(Subcategory__name__icontains=keyword))
           
        else:                  
            return redirect('product_show')
    context={
        'products':products,
        
    }
    return render(request,'adminz/pro_show.html',context)


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def edit_product(request,slug):
    pro =Product.objects.get(slug=slug)
    form=ProductForm(instance=pro)
    try:
        if request.method=='POST':
            form=ProductForm(request.POST  ,request.FILES,instance=pro)
            if  form.is_valid():
                form.save()
                return redirect('product_show')
            else:
               pass     

    except:
        messages.error(request,'is some mistake youhave to made')
        return redirect('edit_product')
    
    context={
        'form':form,
    }
    return render(request,'adminz/pro_edit.html',context)
    
    

@user_passes_test(lambda u: u in account ,login_url='admin_login')
def delete_pro(request,slug):
    pro=Product.objects.get(slug=slug)
    pro.delete()
    return redirect('product_show')


@user_passes_test(lambda u: u in account ,login_url='admin_login')

def add_product(request):
  
    form=ProductForm()
    try:
        if request.method=='POST':
            form=ProductForm(request.POST ,request.FILES)
            if  form.is_valid():
                form.save()
                return redirect('product_show')
            else:
               pass     

    except:
        messages.error(request,'is some mistake youhave to made')
        return redirect('edit_product')
    
    context={
        'form':form,
    }
    return render(request,'adminz/pro_add.html',context)



@user_passes_test(lambda u: u in account ,login_url='admin_login')
    
def load_subcategory(request):
    category_id = request.GET.get('category')
    print(category_id)
    subcategory = SubCategory.objects.filter(category_id=category_id).order_by('name')
    print(subcategory)
    return render(request,'adminz/drop_down.html',{'subcategory': subcategory})




@user_passes_test(lambda u: u in account ,login_url='admin_login')

def Section_show(request):
    section=Section.objects.all()

    context={
        'section':section,
    }
    return render(request,'adminz/section.html',context)



@user_passes_test(lambda u: u in account ,login_url='admin_login')
def sectionsearch(request): 
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        print('hey')
        if keyword:
            section =Section.objects.order_by('-id').filter(Q(name__icontains=keyword) )
           
        else:           
            return redirect('Section_show')
    context={
        'section':section,
        
    }
    return render(request,'adminz/section.html',context)


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def editsection(request,id):    
    try:
        sec=Section.objects.get(id=id)
        form=SectionForm(instance=sec)
        if request.method=='POST':
            form=SectionForm(request.POST ,request.FILES,instance=sec)
            if form.is_valid():
                form.save()
                return redirect('Section_show')

    except:
        messages.error(request,'is some mistake youhave to made')
        return redirect('Section_show')
        
    context={
        'form':form,
    }
    return render(request,'adminz/editsection.html',context)


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def addsection(request):    
    form=SectionForm()
    print('hdkshakjhfhfkdkfsh')
    if request.method=='POST':
        form=SectionForm(request.POST)
        print('111111111')        
        if form.is_valid():
            print('pppppppppp')
            form.save()
            return redirect('Section_show')
    context={
    'form':form,
    }
    return render(request,'adminz/addsection.html',context)


   

@user_passes_test(lambda u: u in account ,login_url='admin_login')
def deletesection(request,id):
    sec=Section.objects.get(id=id)
    sec.delete()
    return redirect('Section_show')


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def discount_Show(request):
    disc=DiscountCoupon.objects.all()
    context={
        'disc':disc,
    }

    return render(request,'adminz/discount.html',context)





@user_passes_test(lambda u: u in account ,login_url='admin_login')
def searchdiscount(request): 
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        print('hey')
        if keyword:
            disc =DiscountCoupon.objects.order_by('-id').filter(Q(coupon_code__icontains=keyword)|Q(discount__icontains=keyword) )
           
        else:           
            return redirect('discount_Show')
    context={
        'disc':disc,
        
    }
    return render(request,'adminz/discount.html',context)





@user_passes_test(lambda u: u in account ,login_url='admin_login')
def edit_discount(request,id):    
    try:
        disc=DiscountCoupon.objects.get(id=id)
        form=DiscountForm(instance=disc)
        if request.method=='POST':
            form=DiscountForm(request.POST,instance=disc)
            if form.is_valid():
                form.save()
                return redirect('discount_Show')

        else:
            context={ 'form':form,}            
            return render(request,'adminz/edit_discount.html',context)
    except:
        messages.error(request,'are you making some problems')
        return redirect('discount_Show')


@user_passes_test(lambda u: u in account ,login_url='admin_login')

def add_discount(request):  
    form=DiscountForm()  
    if request.method=='POST':
        form=DiscountForm(request.POST)
        print('DISCOUNTTTT')
        if form.is_valid():
            print('validddddddddd')
            form.save()
            return redirect('discount_Show')   
    context={
        'form':form,
            }
    return render(request,'adminz/add_discount.html',context)








@user_passes_test(lambda u: u in account ,login_url='admin_login')
def delete_discount(request,id):
    disc=DiscountCoupon.objects.get(id=id)
    disc.delete()
    return redirect('discount_Show')



@user_passes_test(lambda u: u in account ,login_url='admin_login')
def OrderProduct_show(request):
    order=OrderProduct.objects.all()
    context={
        'order':order,
    }
        
    return render(request,'adminz/order.html',context)



@user_passes_test(lambda u: u in account ,login_url='admin_login')
def searchorderproduct(request): 
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        print('hey')
        if keyword:
            order=OrderProduct.objects.filter(Q(user__email__icontains=keyword)|Q(payment__payment_id__icontains=keyword)|Q(product__name__icontains=keyword) )
           
        else:           
            return redirect('OrderProduct_show')
    context={
        'order':order,
        
    }
    return render(request,'adminz/order.html',context)

@user_passes_test(lambda u: u in account ,login_url='admin_login')

def editstatus(request,id):
    try:
        order=Order.objects.get(id=id)
        form=OrderStatusform(instance=order)
        if request.method=='POST':
            form=OrderStatusform(request.POST,instance=order)
            if form.is_valid():
                form.save()
                return redirect('OrderProduct_show')
        context={
            'form':form,
        }
        return render(request,'adminz/editstatus.html',context)

    except:
        messages.error(request,'are you making some problems')
        return redirect('OrderProduct_show')
        


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def charts(request):
    return render(request,'adminz/chat.html')



# def pie_chart(request):
#     labels = []
#     data = []

#     queryset = OrderProduct.objects.order_by('-quantity')
 

#     for x in queryset:
#         labels.append(x.product)
#         data.append(x.quantity)
#         print(x.quantity)
#         print(x.product)
#     print(labels)
#     print(data)

#     return render(request, 'adminz/chat.html', {
#         'labels': labels,
#         'data': data,
#     })


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def quantity_chart(request):
    labels = []
    data = []

    queryset = OrderProduct.objects.values('product__name').annotate(quantity=Sum('quantity')).order_by('-quantity')[:5]
    for entry in queryset:
        labels.append(entry['product__name'])
        data.append(entry['quantity'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def category_chart(request):
    labels = []
    data = []

    queryset = OrderProduct.objects.values('product__category__title').annotate(quantity=Sum('quantity')).order_by('-quantity')[:5]
    for entry in queryset:
        labels.append(entry['product__category__title'])
        data.append(entry['quantity'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
@user_passes_test(lambda u: u in account ,login_url='admin_login')

def variationsshow(request):
    var=Variation.objects.all().order_by('-id')
    context={
        'var':var,
    }

    return render(request,'adminz/variation.html',context)




@user_passes_test(lambda u: u in account ,login_url='admin_login')
def searchvaraition(request): 
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        print('hey')
        if keyword:
            var=Variation.objects.filter(Q(product__name__icontains=keyword) )           
        else:           
            return redirect('variationshow')
    context={
        'var':var,
        
    }
    return render(request,'adminz/variation.html',context)


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def edit_variation(request,id):
    try:
        var=Variation.objects.get(id=id)
        form=VariationForm(instance=var)
        if request.method=='POST':
            form=VariationForm(request.POST,instance=var)
            if form.is_valid():
                form.save()
                return redirect('variationshow')

        context={
            'form': form,
        }
        return render(request,'adminz/edit_variation.html',context)
    except:
        messages.error(request,'are you making some problems')
        return redirect('variationshow')


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def add_variation(request):
    try:
       
        form=VariationForm()
        if request.method=='POST':          
            if form.is_valid():
                form.save()
                return redirect('variationshow')

        context={
            'form': form,
        }
        return render(request,'adminz/add_variation.html',context)
    except:
        messages.error(request,'are you making some problems')
        return redirect('variationshow')

@user_passes_test(lambda u: u in account ,login_url='admin_login')

def delete_variation(request,id):
    var=Variation.objects.get(id=id)
    var.delete()
    return redirect('variationshow')



def adminlogout(request):
    if 'admin' in request.session:
        request.session.flush()
    auth.logout(request)
    messages.info(request,'susessfully loged out')
    return redirect('home')


from .utils import render_to_pdf

@user_passes_test(lambda u: u in account ,login_url='admin_login')
def paymentlist(request):
    template_name = "adminz/homee.html"
    account=Account.objects.filter( is_superadmin=False).count()
    payment=OrderProduct.objects.filter(ordered=True).count()    
    number=OrderProduct.objects.filter(ordered=True)
    transations=Payment.objects.all()  
    
    user=request.user
    sum=0
    for x in number:
        sum+=x.product_price

    pro_count=Product.objects.all().count()


    

    return render_to_pdf(
        template_name,
        {
        'account':account,
        'payment':payment,
        'sum':sum,
        'pro_count':pro_count,
        'transations':transations,
        'user':user,
        # 'pts':products,
        },
    )


@user_passes_test(lambda u: u in account ,login_url='admin_login')   
def brandshow(request):
    brand=Brand.objects.all()
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']       
        if keyword:
            brand=Brand.objects.filter(Q(name__icontains=keyword) )     
   
    return render(request,'adminz/brand.html',{'brand':brand,})


@user_passes_test(lambda u: u in account ,login_url='admin_login')
def edit_brand(request,id):
    brand=Brand.objects.get(id=id)
    form=BrandForm(instance=brand)
    try:
        if request.method =="POST":
            form=BrandForm(request.POST,instance=brand)
            if form.is_valid():
                form.save()
                return redirect('brand')
            else:
                messages.error(request,'error found')
        
    except:
        messages.error(request,'error found')
        return redirect('brand')
    context={
            'form':form,
        }

    return render(request,'adminz/edit_brand.html',context)



@user_passes_test(lambda u: u in account ,login_url='admin_login')
def delete_brand(request,id):
    brand=Brand.objects.get(id=id)
    brand.delete()
    return redirect('brand')




def add_brand(request):
    form=BrandForm()
    try:
        if request.method =="POST":
            form=BrandForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('brand')
            else:
                messages.error(request,'error found')
        
    except:
        messages.error(request,'error found')
        return redirect('brand')
    context={
            'form':form,
        }

    return render(request,'adminz/edit_brand.html',context)


def reviews(request):
    review=Reviews.objects.all()
    # if 'keyword' in request.GET:
    #     keyword=request.GET['keyword']
    #     print('hey')
    #     if keyword:
    #         review=Reviews.objects.filter(Q(user__icontains=keyword)|Q(product__icontains=keyword) )     
    
    return render(request,'adminz/review.html',{'review':review})



def delete_review(request,id):
    review=Reviews.objects.get(id=id)
    review.delete()
    return redirect('review')

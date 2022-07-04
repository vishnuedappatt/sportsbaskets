

from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from category.models import Category,SubCategory
from .models import  Product,Cart,CartItem,Variation, Wishlist,DiscountCoupon,Discount
from  django.core.paginator import Paginator
from django.db.models import  Q
from django.contrib.auth.decorators import login_required
from user.models import Address
from user.forms import AddresssForm
from .models import Reviews
from django.contrib import messages



def home(request):
    if 'admin' in request.session:
        return redirect('adminhome')
    categories=Category.objects.all()
    products=Product.objects.filter(section__name='home')[0:8]
    related_product=Product.objects.all().order_by('-id')[0:8]
    context={
        'category':categories,
        'pro':products,
        'related_product':related_product
    }

    return render(request,'products/test.html',context)






def categories(request,category_slug=None):
    category = None
    products =None    
    subcat=SubCategory.objects.filter(category__slug=category_slug)
    count=0
    if category_slug !=None:
        category=get_object_or_404(Category,slug = category_slug)
        products=Product.objects.filter(category=category)
        paginator =Paginator(products,8)
        page = request.GET.get('page') 
        paged_products=paginator.get_page(page)
        if request.method=="POST":
            sort_id=request.POST['sorting']
            if sort_id=='high':
                products=Product.objects.filter(category=category).order_by('price')
                count=products.count()
                paginator =Paginator(products,6)
                page = request.GET.get('page') 
                paged_products=paginator.get_page(page)
            else:
                products=Product.objects.filter(category=category).order_by('-price')
                count=products.count()
                paginator =Paginator(products,6)
                page = request.GET.get('page') 
                paged_products=paginator.get_page(page)
            
        

    else:
        products = Product.objects.all()
    context={
        'products':paged_products,
        'subcat':subcat,
        'categor':category,
        'count':count,
       
    }
    return render(request,'products/categorylist.html',context)

  
def subcategories(request,category_slug,subcategory_slug):
    count=0
    subcategory =get_object_or_404(SubCategory,slug=subcategory_slug)
    products=Product.objects.filter(Subcategory=subcategory)
    count=products.count()
    paginator =Paginator(products,6)
    page = request.GET.get('page') 
    paged_products=paginator.get_page(page)
    if request.method=="POST":
        sort_id=request.POST['sorting']
        if sort_id=='high':
            products=Product.objects.filter(Subcategory=subcategory).order_by('price')
            count=products.count()
            paginator =Paginator(products,6)
            page = request.GET.get('page') 
            paged_products=paginator.get_page(page)
        else:
            products=Product.objects.filter(Subcategory=subcategory).order_by('-price')
            count=products.count()
            paginator =Paginator(products,6)
            page = request.GET.get('page') 
            paged_products=paginator.get_page(page)
        
    context={
        'products':paged_products,
        'count':count, 
    }
    return render(request,'products/subcategory.html',context)




def product_detail(request,category_slug,subcategory_slug,product_slug):
 
    item=Product.objects.get(slug=product_slug)
    rating=0
    Star=0
    try:
        single_product=Product.objects.get(category__slug=category_slug,Subcategory__slug=subcategory_slug,slug=product_slug)
        related_product=Product.objects.filter(Subcategory__slug=subcategory_slug)[0:5]
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        review=Reviews.objects.filter(product=item)
        # review=Reviews.objects.filter(product=item) 
        reviewcount=review.count()
        if reviewcount >0:
            for rate in review:
                if rate.rating:
                    rating+=rate.rating
            Star=int(rating/reviewcount)

    
    except Exception as e:
        raise e 

    context={
        
        'single_product':single_product,
        'related_product':related_product,
        'in_cart':in_cart,     
        'reviewcount':reviewcount,
        'review':review,
        'star':Star,
    }
    return render(request,'products/product_detailes.html',context)



def search(request): 
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        print('hey')
        if keyword:
            products =Product.objects.order_by('-id').filter(Q(name__icontains=keyword) | Q(category__title__icontains=keyword) | Q(brand__name__icontains=keyword) | Q(Subcategory__name__icontains=keyword))
            count=products.count() 
        else:
            messages.success(request,'no items found')
            return redirect('home')
    context={
        'products':products,
        'count':count,
    }
    return render(request,'products/subcategory.html',context)




def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart




def add_cart(request,product_id):
    current_user=request.user
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        product_variation=[]
        if request.method =='POST':
            for item in request.POST:
                key = item
                value=request.POST[key]
                print('hljmklfmlkfmlkfmlmf')
                print(key,value)

                try:
                    print('3435435454')
                    variation =Variation.objects.get(product=product,variation_category__iexact= key,variation_value__iexact=value)
                    product_variation.append(variation)
                    print('value is')
                    print(variation)

                except:
                    print('hi')
                    pass       
    
        
       

        is_cart_item_exists= CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,user=current_user)
            ex_var_list=[]
            id=[]

            for item in cart_item:
                existing_variation =item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)

            if product_variation in ex_var_list:     #incresing cart item
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                if (product.stock-item.quantity)>0:
                    item.quantity +=1
                    item.save()
                else:
                    messages.error(request,'No more stock available')
                    return redirect('cart')
                # keep=Wishlist.objects.filter(user=request.user,product=product)
                # print('heyyyyyy0000y')
                # if item in keep:
                #     print('qweweer')
                #     keep.delete()     
            
            
            else:
                item = CartItem.objects.create(product=product,quantity=1,user=current_user) #create for several variation contains several product
                if len(product_variation) > 0: #checking the variation available or not
                    item.variations.clear()                
                    item.variations.add(*product_variation)  
                    # keep=Wishlist.objects.filter(user=request.user,product=product)
                    # print('tetrrt')
                    # if item in keep:
                    #     print('haaaapp')
                    #     keep.delete()     
                cart_item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1,user=current_user)
            if len(product_variation) > 0:
                cart_item.variations.clear()           
                cart_item.variations.add(*product_variation)
                keep=Wishlist.objects.filter(user=request.user,product=product)
                if cart_item in keep:
                    print('ooooooo')
                    keep.delete()     
            cart_item.save()
            print(cart_item.product)
        return redirect('cart')

            

    else:
        product_variation=[]
        if request.method =='POST':
            for item in request.POST:
                key = item
                value=request.POST[key]
                print('hljmklfmlkfmlkfmlmf')
                print(key,value)

                try:
                    print('3435435454')
                    variation =Variation.objects.get(product=product,variation_category__iexact= key,variation_value__iexact=value)
                    product_variation.append(variation)
                    print('value is')
                    print(variation)

                except:
                    print('hi')
                    pass       
      
        product = Product.objects.get(id=product_id) #get the product
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart using cart_id in the session

        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))

        cart.save()


        is_cart_item_exists= CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,cart=cart)
            ex_var_list=[]
            id=[]

            for item in cart_item:
                existing_variation =item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)

            if product_variation in ex_var_list:     #incresing cart item
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                if (product.stock-item.quantity)>0:
                    item.quantity +=1
                    item.save()
                else:
                    messages.error(request,'No more stock available')
                    return redirect('cart')
            

                
                 
            else:
                item = CartItem.objects.create(product=product,quantity=1, cart=cart) #create for several variation contains several product
                if len(product_variation) > 0: #checking the variation available or not
                    item.variations.clear()                
                    item.variations.add(*product_variation)                                                
                # changed here
                item.save()
                
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                cart_item.variations.clear()           
                cart_item.variations.add(*product_variation)
            cart_item.save()
            
            
            print(cart_item.product)
        return redirect('cart')






def remove_cart(request, product_id,cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
             cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id )


        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id )

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')  

def remove_cartitem(request, product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id )

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id )
   
   
    cart_item.delete()
    return redirect('cart')



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True).order_by('-id')
            for x in cart_items:
                if x.product.stock <=0:
                    messages.error(request,'Not enough stock right now')
                

                if x.product.stock < x.quantity:
                     x.quantity=x.product.stock
                     x.save()
                
        
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('-id')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' :grand_total,
    }
    return render(request,'products/cart.html',context)






@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax=0
    grand_total=0
    address=0

    if request.method=='POST':
        form=AddresssForm(request.POST)        
        if form.is_valid():           
            data=Address()
            data.user=request.user
            data.first_name =form.cleaned_data['first_name']
            data.last_name =form.cleaned_data['last_name']
            data.email =form.cleaned_data['email']
            data.phone =form.cleaned_data['phone']
            data.address_line_1 =form.cleaned_data['address_line_1']
            data.address_line_2 =form.cleaned_data['address_line_2']
            data.city =form.cleaned_data['city']
            data.district =form.cleaned_data['district']
            data.state =form.cleaned_data['state']
            data.country =form.cleaned_data['country']
            data.zip =form.cleaned_data['zip']
            data.save()
            return redirect ('checkout')
        else:
            if not 'coupon' in request.POST :
                messages.error(request,'Please enter correct data /or please avoid auto added data(suggessions) please type manuely')
      
    try:
        tax=0
        grand_total=0
        start=0
        discount=0
        discount_available=0
        code=None
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
            address=Address.objects.filter(user=request.user)
            coupon=DiscountCoupon.objects.all()

            if request.method=='POST':
                count=Discount.objects.filter(user=request.user).exists()
                if count:
                    Discount.objects.filter(user=request.user).delete()   
                try:                                                    
                    coupon=request.POST['coupon']
                    code=DiscountCoupon.objects.get(coupon_code=coupon)           
                    discount=code.discount                    
                    start=code.active_from
                    messages.success(request, 'coupon appleid succesfully')
                except:
                    discount=Discount.objects.filter(user=request.user)
                    discount.delete()
                    return redirect('checkout')

                data=Discount()
                data.user=request.user
                data.discount_appiled=discount
                data.save()
            
              
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)        
            quantity += cart_item.quantity
        tax = (2*total) / 100
        grand_total_without = total + tax

        # coupon added for discount


        if grand_total_without >=start:
            discount_available=discount*(grand_total_without)
            grand_total=(grand_total_without)-discount_available

    except ObjectDoesNotExist:
        return redirect('checkout')

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' :grand_total,
        'address':address,
        'code':code,
        'discount_available':discount_available,
        'grand_total_without':grand_total_without,
        'coupon':coupon,

    }

    return render(request,'products/check.html',context)




@login_required(login_url='login')

def wishlist_add(request,id):    
    data=Wishlist()
    user=request.user    
    product=Product.objects.get(id=id)
    wish=Wishlist.objects.filter(product=product,user=user).exists()
    print('pass')
    if not  wish:
        print('gettttt')
        product=Product.objects.get(id=id)
        data.product=product
        data.user=user    
        data.save() 
    print('almost')
    return redirect('home')


@login_required(login_url='login')
def wishlist(request):
    user=request.user
    products=Wishlist.objects.filter(user=user)
    context={
        'product':products
    }
    return render(request,'products/wishlist.html',context)


@login_required(login_url='login')
def wishlist_remove(request,id):
    product=Wishlist.objects.get(id=id)
    product.delete()
    return redirect('wishlist')



def remove_address(request,id):
  add=Address.objects.get(id=id)
  add.delete()
  return redirect('checkout')







   
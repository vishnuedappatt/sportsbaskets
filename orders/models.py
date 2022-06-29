from django.db import models
from user.models import Account
from products.models import Product,Variation
from  user.models import Address

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100)
    amount_paid=models.CharField(max_length=100)
    order_id=models.CharField(max_length=50)
    paid=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.payment_id




class Order(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Confirmed','Confirmed'),
        ('Cancelled','Cancelled'),
        ('Failed','Failed'),
        ('Delivered','Delivered'),
    )
   

    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number=models.CharField(max_length=20)
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)    
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
   
    ip=models.CharField(max_length=20 ,blank=True)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.order_number  

 


class OrderProduct(models.Model):
    METHOD={
        ('Pay','Pay'),
        ('Razorpay','Razorpay'),
        ('COD','COD'),
    }
    order= models.ForeignKey(Order,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    varation=models.ForeignKey(Variation,on_delete=models.SET_NULL,null=True,blank=True)   
    quantity=models.IntegerField()
    product_price=models.FloatField()
    method=models.CharField(max_length=15,choices=METHOD,null=True,blank=True)
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
 



    def __str__(self):
        return self.product.name








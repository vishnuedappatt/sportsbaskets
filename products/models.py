from django.db import models
from category.models import *
from user.models import *


# Create your models here.
class Section(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name=models.CharField(max_length=20)


    def __str__(self):
        return self.name



class Product(models.Model):
    category     =models.ForeignKey(Category,on_delete=models.CASCADE)
    Subcategory  =models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    name         =models.CharField(max_length=50)
    slug         =models.SlugField(unique=True)
    description  =models.TextField(max_length=200)
    price        =models.DecimalField(max_digits=6,decimal_places=2)
    section      =models.ForeignKey(Section,on_delete=models.CASCADE,blank=True,null=True)
    discount     =models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    image        =models.ImageField(upload_to='gallery',null=True,blank=True)
    stock        =models.IntegerField()
    brand        =models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,blank=True)
    availability =models.BooleanField()
    created_at   =models.DateTimeField(auto_now_add=True)
    modified_at  =models.DateTimeField(auto_now=True)
     

    def __str__(self):
        return self.name 


    def get_url(self):
        return reverse ('product_detail',args=[self.category.slug,self.Subcategory.slug,self.slug])





# class VariationManager(models.Manager):
#     def sizes(self):
#         return super(VariationManager,self).filter(variation_category='size',is_active=True)


    # def inchs(self):
    #     return super(VariationManager,self).filter(variation_category='inch',is_active=True)



variation_category_choice=(
    ('size','size'),

)



class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value =models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.variation_value





class Cart(models.Model):
    cart_id=models.CharField(max_length=200,blank=True)
    date_added=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product =models.ForeignKey(Product,on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variation,blank=True)
    cart    =models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)

       
    def sub_total(self):
        return self.product.price * self.quantity
        
    def __unicode__(self):
        return self.product


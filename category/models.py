from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(unique=True,max_length=50)
    image=models.ImageField( upload_to='category' ,null=True,blank=True)
    

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('categorylist',args=[self.slug])


class SubCategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name =models.CharField(max_length=50)
    slug =models.SlugField(unique=True)


    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('subcategorylist',args=[self.category.slug,self.slug])



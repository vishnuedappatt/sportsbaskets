from django import forms
from category.models import Category,SubCategory
from products.models import Product, DiscountCoupon,Section,Variation,Brand
from orders.models import Order




class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['title','image','slug']


    def _init_(self, *args, **kwargs):
        super(CategoryForm, self)._init_(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})




class SubCategoryForm(forms.ModelForm):
    class Meta:
        model=SubCategory
        fields=['category','name','slug']

    def __init__(self, *args, **kwargs):
        super(SubCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})




class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['category','Subcategory','name','slug','description','price','section','image','image1','image2','image3','stock','brand','availability']


    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['Subcategory'].widget.attrs.update({'class': 'form-control'})    
        self.fields['section'].widget.attrs.update({'class': 'form-control'})
        self.fields['brand'].widget.attrs.update({'class': 'form-control'})    
       
        self.fields['Subcategory'].queryset=SubCategory.objects.none()



        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['Subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['Subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')





class SectionForm(forms.ModelForm):
    class Meta:
        model=Section
        fields=['name']


class DiscountForm(forms.ModelForm):
    class Meta:
        model=DiscountCoupon
        fields=['coupon_code','discount','active_from']



class OrderStatusform(forms.ModelForm):
    class Meta:
        model=Order
        fields=['status']
    def __init__(self, *args, **kwargs):
        super(OrderStatusform, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        



class VariationForm(forms.ModelForm):
    class Meta:
        model=Variation
        fields=['product','variation_category','variation_value','is_active']
    def __init__(self, *args, **kwargs):
        super(VariationForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['variation_category'].widget.attrs.update({'class': 'form-control'})
        self.fields['variation_value'].widget.attrs.update({'class': 'form-control'})


class BrandForm(forms.ModelForm):
    class Meta:
        model=Brand
        fields=['name']

    def __init__(self,*args, **kwargs):
        super(BrandForm,self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
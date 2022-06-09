import imp
from pyexpat import model
from django import forms
from  . models import Account,Address



class RegistrationForm(forms.ModelForm):
    password =forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'enter password'}))
    confirm_password =forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'confirm password'}))
    class Meta:
        model  = Account
        fields =['first_name','last_name','phone_number','email','password']



    def __init__(self, *args ,**kwargs):
        super(RegistrationForm,self).__init__(*args ,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter first name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter last name'
        self.fields['email'].widget.attrs['placeholder']='Enter email'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter phone number'

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')





class AddresssForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['first_name','last_name','email','phone','address_line_1','address_line_2','city','district','state','country','zip']
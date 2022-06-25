from dataclasses import fields
import imp
from pyexpat import model
from xml.dom import ValidationErr
from django import forms
from requests import request
from  . models import Account,Address
from django.contrib import messages



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

    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        phone_number=cleaned_data.get('phone_number')

        if password !=confirm_password:
            
            raise forms.ValidationError(
                'password doesnot match...'
                
            )
        if len(password)<8:
            raise forms.ValidationError(
                'password Mismatch'
            )
            
        if len(phone_number) !=10:
            raise forms.ValidationError(
                'please enter valid number'
            )
        



class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')





class AddresssForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['first_name','last_name','email','phone','address_line_1','address_line_2','city','district','state','country','zip']


class  EditProfileForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=['first_name','last_name','username']
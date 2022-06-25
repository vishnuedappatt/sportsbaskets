from django import forms
from . models import Reviews




class ReviewForm(forms.ModelForm):
    class Meta:
        model=Reviews
        fields=['description','image']


    def __init__(self, *args, **kwargs):
            super(ReviewForm, self).__init__(*args, **kwargs)
            self.fields['image'].widget.attrs.update({'class': 'form-control'})
            self.fields['description'].widget.attrs.update({'class': 'form-control'})
            
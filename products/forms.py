from django import forms
from .models import Product, BuyOffer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'image', 'description', 'price', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': '상품명을 입력해주세요',
                'maxlength': '40',
                'class': 'form-input',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': '상품의 상태, 특징 등을 자세히 적어주세요',
                'maxlength': '500',
                'class': 'form-textarea',
                'rows': 5,
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': '가격을 입력해주세요',
                'class': 'form-input',
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-file', 'id': 'id_image_input'}),
        }


class BuyOfferForm(forms.ModelForm):
    class Meta:
        model = BuyOffer
        fields = ['price']
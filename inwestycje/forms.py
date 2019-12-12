from datetime import date

from django import forms

from inwestycje.models import Product, Category


class AddProductForm(forms.ModelForm):
    start_date = forms.DateField(input_formats=["%d.%m.%Y"])
    end_date = forms.DateField(input_formats=["%d.%m.%Y"])

    class Meta:
        model = Product
        exclude = ['user']


class LoginForm(forms.Form):
    name = forms.CharField(max_length=164)
    password = forms.CharField(widget=forms.PasswordInput())


class DeleteProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductModifyForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'profitability', 'start_date', 'end_date', 'files']
        labels = {
            'name': 'name',
            'description': 'description',
            'profitability': 'profitability',
            'start_date': 'start_date',
            'end_date': 'end_date',
            'files': 'files',
        }



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryModifyForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'name',

        }



from django import forms
from .models import Client, Produit, Commande, Detail
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 

class ClientForm(forms.ModelForm):
    class Meta:
        model  = Client
        fields = '__all__'


class ProduitForm(forms.ModelForm):
    class Meta:
        model  = Produit
        fields = '__all__'


class CommandeForm(forms.ModelForm):
    class Meta:
        model  = Commande
        fields = '__all__'


class DetailForm(forms.ModelForm):
    class Meta:
        model  = Detail
        fields = '__all__'



class RegisterForm(UserCreationForm):
    email = forms.EmailField(label ='Adresse Email',required =True)
    class Meta :
        model = User 
        fields=['username','email','password1','password2']
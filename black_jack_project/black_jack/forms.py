from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.CharField(max_length=20,widget= forms.EmailInput)
    password = forms.CharField(max_length=20,widget= forms.PasswordInput)
    confirm = forms.CharField(max_length=20,widget= forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20,widget= forms.PasswordInput)
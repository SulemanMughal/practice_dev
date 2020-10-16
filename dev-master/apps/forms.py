from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import *
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,)
import re

# User Login Form ................


class loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

# User Registration Form...................


class registerForm(forms.ModelForm):
    # username = forms.CharField(label='Username', widget = forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
    ), strip=False, help_text=password_validation.password_validators_help_text_html(),)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(
    ), strip=False, help_text="Both Passwords should be same.",)
    email = forms.EmailField(label='Email Address', widget=forms.TextInput())

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
        ]
    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     if User.objects.filter(username=username).exists():
    #         raise ValidationError("Username exists")
    #     return username

    # Cleaning Method for password Match..........

    def clean_password2(self):
        cd = self.cleaned_data
        if self.cleaned_data.get('password') != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']


    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with that Email Address already exists")
        return email

    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("User with that Email Address already exists")
       return self.cleaned_data

# User Can Edit his profile using this Form..........................


class EditProfileForm(UserChangeForm):
    password = forms.CharField(
        label='', widget=forms.TextInput(attrs={'type': 'hidden'}))

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'password',
                  ]


A = (re.compile("\d\d\d-\d\d\d-\d\d\d\d"))

# User Extra Information ................


class profileInformForm(forms.ModelForm):
    class Meta:
        model = profileModel
        fields = ['contactNumber']

    def clean(self):
        contactNumber = self.cleaned_data.get("contactNumber")
        if A.match(str(contactNumber)):
            if profileModel.objects.filter(contactNumber=str(contactNumber)).exists():
                # print(self.__dict__)
                raise forms.ValidationError("Contact Number already exists.")
            else:
                return self.cleaned_data
        else:
            raise forms.ValidationError(
                "Please enter contact number in correct format")


# User Extra Information ................
class EditprofileInformForm(forms.ModelForm):
    class Meta:
        model = profileModel
        fields = ['contactNumber']

    def clean(self):
        contactNumber = self.cleaned_data.get("contactNumber")
        if A.match(str(contactNumber)):
            if profileModel.objects.filter(contactNumber=str(contactNumber)).exists():
                if self.__dict__['instance'].id == profileModel.objects.get(contactNumber=str(contactNumber)).id:
                    return self.cleaned_data
                else:
                    raise forms.ValidationError(
                        "Contact Number already exists.")
            else:
                return self.cleaned_data
        else:
            raise forms.ValidationError(
                "Please enter contact number in correct format")



class contactForm(forms.Form):
    userName = forms.CharField(
        label='', widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    body = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'Message', 'cols': '30', 'rows': '10'}))


class planForm(forms.ModelForm):
    class Meta:
        model = plan
        exclude = ['user', 'currentFamilySize', 'status', 'linkWeb', 'familySize'
                   ]
        widgets = {
            'total_slots': forms.Select(choices=[(int(i), int(i)) for i in range(1, 13)])
        }

# ****************************************************************
# Plan Comment Form
# ****************************************************************


class planCommentForm(forms.ModelForm):
    class Meta:
        model = commentPlan
        fields = [
            'message'
        ]


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'customer_id']


class PayPalForm(forms.ModelForm):
    class Meta:
        model = PayPal
        exclude = ['user']

from django import forms
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
import datetime


class add_ingredient(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name', 'quantity', 'unit', 'unit_price')

class update_ingredient(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name', 'quantity', 'unit', 'unit_price')


class add_menu(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('title', 'price')

class add_required_ingredient(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ('menu_item', 'ingredient', 'quantity_Required')

class add_purchase(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('menu_item', 'timestamp')
        Purchase.timestamp = datetime.datetime.now()




from django.contrib.auth.models import User


class UserCreateForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username",)
        help_texts = {
            'username': None,
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

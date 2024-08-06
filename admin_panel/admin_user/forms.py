from accounts.models import User, Profile
from django import forms
from django.forms import ModelForm


class UserForm(ModelForm):
    """
    UserForm class

    This From used to make form of User

    Parameters
    ----------
    ModelForm : django.forms

    """

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   }


class ProfileForm(ModelForm):
    """
    ProfileForm class

    This From used to make form of Profile

    Parameters
    ----------
    ModelForm : django.forms

    """

    class Meta:
        model = Profile
        fields = '__all__'

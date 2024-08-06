from  django import forms
from apis.admin_site_management.models import FAQ
class FAQForm(forms.ModelForm):
    class Meta:
        model=FAQ
        fields="__all__"
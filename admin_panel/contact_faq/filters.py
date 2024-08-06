import django_filters
from apis.admin_site_management.models import Contact,FAQ


class ContactFilter(django_filters.FilterSet):
    class Meta:
        model = Contact
        fields =['name']


class FAQFilter(django_filters.FilterSet):
    class Meta:
        model = FAQ
        fields = ['title']
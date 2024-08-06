import django_filters
from accounts.models import User, Profile


class UserFilter(django_filters.FilterSet):
    """
    User filters
    """

    class Meta:
        model = User
        fields = ['username']


class ProfileFilter(django_filters.FilterSet):
    """
    Filters for Profile
    """

    class Meta:
        model = Profile
        fields = ['user']

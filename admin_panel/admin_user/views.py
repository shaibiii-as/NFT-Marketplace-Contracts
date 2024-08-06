from accounts.models import User, Profile
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .filters import UserFilter, ProfileFilter


class ListUserView(View):
    """
    **ListUerView class**

    This view used to perform get request on user object to view the list of user object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request):
        """
        Http get request use to Render home2 template,

        **Template:**

        `template:` admin_user/home2.html

        **Returns:**

        `render:` home2 template

        """
        user = User.objects.all().order_by('id')
        user_count = user.count()
        myfilter = UserFilter(request.GET, queryset=user)
        user = myfilter.qs
        p = Paginator(user.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'home2.html',
                      {'users': user, 'myfilter': myfilter, 'obj': obj, 'user_count': user_count})


class DeleteUserView(View):
    """
    **DeleteUserView class**

    This view used to perform get  request on User object to delete the User object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request, id):
        """
        Http get request use to Render list User template after delete the user.

        **Template:**

        `template:` admin_user/home2.html

        **Returns:**

        `HttpResponseRedirect:` home2 template

        """
        object = User.objects.get(id=id)
        object.is_active = False
        object.save()
        url = reverse('admin_user:home')
        return HttpResponseRedirect(url)


class ListProfileView(View):
    """
    **ListCollectionView class**

    This view used to perform get request on profile object to view the list of profile object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request):
        """
        Http get request use to Render profiles template

        **Template:**

        `template:` admin_user/profiles.html

        **Returns:**

        `render:` profile template and user list

        """
        profile_obj = Profile.objects.all().order_by('id')
        pfilter = ProfileFilter(request.GET, queryset=profile_obj)
        profile_obj = pfilter.qs
        p = Paginator(profile_obj.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'profiles.html', {"profile_obj": profile_obj, 'pfilter': pfilter, 'obj': obj})


class DeleteProfileView(View):
    """
    **DeleteProfileView class**

    This view used to perform get  request on profile object to delete the profile object

    **Parameters**

    `View:`  django.views

    """

    def get(self, request, id):
        """
        Http get request use to Render profiles template after delete the profile.

        **Template:**

        `template:` admin_user/profiles.html

        **Returns:**

        `HttpResponseRedirect:` profile list template

        """
        object = Profile.objects.get(id=id)
        object.is_active = False
        object.save()
        url = reverse('admin_user:profiles')
        return HttpResponseRedirect(url)


class ListUserProfileView(View):
    """
    **ListCollectionView class**

    This view used to perform get request on profile object to view the list of profile object

    **Parameters**

    `View:`  django.viewsgit

    """

    def get(self, request, id):
        """
        Http get request use to Render profiles template

        **Template:**

        `template:` admin_user/profiles.html

        **Returns:**

        `render:` profile template and user list

        """
        try:
            profile = Profile.objects.get(user_id = id)
        except Exception as e:
            profile = None
            return render(request, 'profile_view.html',{'profile':profile})


        return render(request, 'profile_view.html',{'profile':profile})

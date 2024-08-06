from django.urls import path

from . import views

app_name = 'admin_user'
urlpatterns = [
    path('home/', views.ListUserView.as_view(), name='home'),
    path('profiles/', views.ListProfileView.as_view(), name='profiles'),
    path('profiles_view/<int:id>/', views.ListUserProfileView.as_view(), name='profiles_view'),
    path('delete_profile/<int:id>/', views.DeleteProfileView.as_view(), name='deleteprofile'),
    path('delete/<int:id>/', views.DeleteUserView.as_view(), name='deletepost')
]

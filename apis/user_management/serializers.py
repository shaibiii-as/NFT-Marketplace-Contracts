from accounts.models import *
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


# from apis.nft_management.serializers import CollectionSerializer

class ProfileSerializer(ModelSerializer):
    """
    Serializer for User Profile
    """

    class Meta:
        model = Profile
        fields = ['vine_link', 'profile_image', 'banner_image', 'about', 'vine_link',
                  'facebook_link', 'twitter_link', 'google_plus_link']


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for Password
    """
    password = serializers.CharField(required=True)


class UserDetailSerializer(UserSerializer):
    """
    Serializer for User Detail
    """
    user_profile = ProfileSerializer(read_only=True, many=True)

    # user_collection = CollectionSerializer(read_only=True, many=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('user_profile', 'user_collection', 'email', 'first_name', 'last_name')


class CustomUserSerializer(UserSerializer):
    """
    Serializer for User
    """
    user_profile = ProfileSerializer(read_only=False)

    class Meta(UserSerializer.Meta):
        Model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'user_profile')
        read_only_fields = ('email',)

    def update(self, instance: User, validated_data):
        profile = validated_data('user_profile')
        instance.first_name = profile['first_name']
        instance.last_name = profile['first_name']
        instance.username = profile['username']
        instance.save()
        if Profile.objects.filter(user=instance).count() == 0:
            Profile.objects.create(**profile, user=instance)
        else:
            Profile.objects.filter(user=instance).update(**profile)
        return instance

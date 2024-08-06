import requests
from accounts.models import *
from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import PasswordResetSerializer, UserDetailSerializer, CustomUserSerializer
from .serializers import ProfileSerializer


@api_view(['GET'])
def activate_user_view(request, uid, token):
    """
    Api for activating user
    """
    post_url = "https://nft-marketeplace-fkg7q.ondigitalocean.app/api/auth/users/activation/"
    post_data = {"uid": uid, "token": token}
    print(post_url)
    print(post_data)
    result = requests.post(post_url, data=post_data)
    message = "Account activate successfully" if (
            result.status_code == 200 or result.status_code == 204) else "Account activation failed"
    return Response({"message": message}, str(result.status_code))


@api_view(['POST'])
def password_reset_view(request, uid, token):
    """
    Api for password reset
    """
    data = request.data
    serializer = PasswordResetSerializer(data=data)
    if serializer.is_valid():
        post_url = "https://nft-marketeplace-fkg7q.ondigitalocean.app/api/auth/users/reset_password_confirm/"
        post_data = {"uid": uid, "token": token, 'new_password': data['password']}
        result = requests.post(post_url, data=post_data)
        content = result.text
        return Response({"content": content, "result": result}, '200')
    else:
        return Response(serializer.errors, '400')


class LogoutAPIView(APIView):
    """
    Class for Logout
    """

    @swagger_auto_schema(
        responses={
            200: "OK",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
        Api for logout
        """
        try:
            refresh_token = request.data.get('refresh_token')
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response({"message": "Logout Sccessfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Message": "Something Went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileManagement(APIView):
    """
        ProfileVManagementView class

        This view performs GET,POST operations for Profile Model

        Parameters
        ----------
        APIView : rest_framework.views

    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        """
            HTTP GET request

            A HTTP endpoint that deletes a Contacts for provided PK

            Parameters
            ----------
            request : django.http.request

            pk : integer


            Returns
            -------
            rest_framework.response
            returns success message if data deleted successfully,error message otherwise
        """
        try:
            prof_obj = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(prof_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"message": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=ProfileSerializer,

        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """
            HTTP PUT request

           A HTTP endpoint that updates a Profile object for provided PK

           Parameters
           ----------
           request : django.http.request

           pk : integer


           Returns
           -------
           rest_framework.response
              returns success message if data updated successfully,error message otherwise
        """
        try:
            profile_obj = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(profile_obj)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        except Profile.DoesNotExist:
            return Response({"message": "Profile does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def delete(self, request, pk):
        """
            HTTP DELETE request

            A HTTP endpoint that deletes a Profile for provided PK

            Parameters
            ----------
            request : django.http.request

            pk : integer


            Returns
            -------
            rest_framework.response
             returns success message if data deleted successfully,error message otherwise
         """
        try:
            nft = Profile.objects.get(pk=pk)
            nft.delete()
            return Response({"message": "Profile deleted successfully"}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"message": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateProfile(APIView):
    """
       CreateProfileView class

      This view performs GET,POST operations for Profile Model

      Parameters
      ----------
      APIView : rest_framework.views

    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
            HTTP POST request

            A HTTP endpoint that saves a Profile object  in DB


            Parameters
            ----------
            request : django.http.request

            Returns
            -------
             rest_framework.response
             returns success message if data saved successfully,error message otherwise
        """
        try:
            user = request.user
            serializer = CustomUserSerializer(data=request.data, instance=user)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetProfileList(APIView):
    """
        ProfileView class

        This view performs GET operations

        Parameters
        ----------
        APIView : rest_framework.views
        """

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request, format=None):
        """HTTP GET request

              A HTTP endpoint that returns Profile objects list

              Parameters
              ----------
              request : django.http.request

              pk : integer


              Returns
              -------
              rest_framework.response
                  returns HTTP 200 status if data returned successfully,error message otherwise
              """
        try:
            profile = Profile.objects.all()
            serializer = ProfileSerializer(profile, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailView(ListAPIView):
    """
    API for User Details with NFT,Collection and user profie
    """
    model = User
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        return User.objects.all()


@api_view(['GET'])
def users_profile_list(request):
    """

    Parameters
    ----------
    request

    Returns: users object
    -------

    """
    try:
        user_obj = Profile.objects.filter(is_removed=False).annotate(user_name=F('user__first_name')).values(
            'user_name', "profile_image")
        return Response({"users_list": user_obj}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

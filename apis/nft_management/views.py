from accounts.models import Profile
from django.db.models.expressions import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from .models import *
from .serializers import NFTSerializer, CollectionSerializer, CategorySerializer, FavouriteNftSerializer, \
    ReportedNftSerializer


class LoggingView(LoggingMixin, generics.GenericAPIView):
    def get(self, request):
        return Response('with logging')


class NFTCreateView(APIView):
    """
    NFTCreateView class

    This view performs POST operation for NFT

    Parameters
    ----------
    APIView : rest_framework.views

    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=NFTSerializer,

        responses={
            201: "CREATED",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
        HTTP POST request

        An HTTP endpoint that saves a NFT object in DB

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns success message if data saved successfully,error message otherwise
        """

        try:
            data = request.data
            data['owner'] = request.user.id
            serializer = NFTSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NFTManagementView(APIView):
    """
        NFTManagementView class

        This view performs PUT & Delete operation for NFT

        Parameters
        ----------
        APIView : rest_framework.views

    """

    permission_classes = [IsAdminUser, IsAuthenticated]

    @swagger_auto_schema(
        request_body=NFTSerializer,

        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """
            HTTP PUT request

            An HTTP endpoint that updates a NFT object for provided PK

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
            nft_object = Nft.objects.get(pk=pk)
            serializer = NFTSerializer(nft_object, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Nft.DoesNotExist:
            return Response({"message": "NFT does not exist"}, status=status.HTTP_400_BAD_REQUEST)

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

            An HTTP endpoint that deletes a NFT object for provided PK

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
            nft = Nft.objects.get(pk=pk)
            nft.is_removed = True
            nft.save()
            return Response({"message": "NFT deleted Successfully"}, status=status.HTTP_200_OK)

        except Nft.DoesNotExist:
            return Response({"message": "NFT does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NFTView(APIView):
    """
        NFTView Class

        This view performs GET operation for NFT

        Parameters
        ----------
        APIView : rest_framework.views

    """

    def get(self, request, pk):
        """
            HTTP GET request

            An HTTP endpoint that returns NFT object for provided PK

            Parameters
            ----------
            request : django.http.request

            pk : integer

            Returns
            ---------
            rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            nft_object = Nft.objects.get(pk=pk)
            serializer = NFTSerializer(nft_object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Nft.DoesNotExist:
            return Response({"message": "NFT does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NFTListView(APIView, LoggingMixin):
    """
        NFTListView Class

        This view performs GET operation for NFT

        Parameters
        ----------
        APIView : rest_framework.views

    """

    def get(self, request):
        """
            HTTP GET request

            An HTTP endpoint that returns all NFT objects

            Parameters
            ----------
            request : django.http.request

            Returns
            -------
            rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            nft = Nft.objects.filter(is_removed=False)
            serializer = NFTSerializer(nft, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Collection.DoesNotExist:
            return Response({"message": "FAQ does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateCollectionView(APIView):
    """
        CreateCollectionView Class

        This view performs POST operation for collection object

        Parameters
        ----------
        APIView : rest_framework.views

    """
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=CollectionSerializer,
        responses={
            201: "CREATED",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
            HTTP POST request

            An HTTP endpoint that saves a collection object in DB

            Parameters
            ----------
            request : django.http.request

            Returns
            -------
            rest_framework.response
            returns success message if data saved successfully,error message otherwise
        """
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = CollectionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionManagementView(APIView):
    """
        CollectionManagementView Class

        This view performs PUT & Delete operation for collection object

        Parameters
        ----------
        APIView : rest_framework.views

    """

    permission_classes = [IsAdminUser, IsAuthenticated]

    @swagger_auto_schema(
        request_body=CollectionSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """
            HTTP PUT request

            An HTTP endpoint that updates a Collection object for provided PK

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
            collection_obj = Collection.objects.get(pk=pk)
            serializer = CollectionSerializer(collection_obj, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Collection.DoesNotExist:
            return Response({"message": " collection does not exist"}, status=status.HTTP_400_BAD_REQUEST)

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

            An HTTP endpoint that deletes a Collection object for provided PK

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
            coll_obj = Collection.objects.get(pk=pk)
            coll_obj.is_removed = True
            coll_obj.save()
            return Response({"message": "collection deleted Successfully"}, status=status.HTTP_200_OK)

        except Collection.DoesNotExist:
            return Response({"message": "collection does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionView(APIView):
    """
        CollectionView Class

        This view performs GET operation for collection object

        Parameters
        ----------
        APIView : rest_framework.views

    """

    def get(self, request, pk):
        """
            HTTP GET request

            An HTTP endpoint that returns collection object for provided PK

            Parameters
            ----------
            request : django.http.request

            pk : integer

            Returns
            ---------
            rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            collection = Collection.objects.get(pk=pk)
            serializer = CollectionSerializer(collection)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Collection.DoesNotExist:
            return Response({"message": "Collection does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionListView(APIView):
    """
        CollectionListView Class

        This view performs GET operation for collection object

        Parameters
         ----------
        APIView : rest_framework.views

    """

    def get(self, request):
        """
            HTTP GET request

            An HTTP endpoint that returns all Collection objects

            Parameters
             ----------
            request : django.http.request

            Returns
            -------
            rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            collection = Collection.objects.filter(is_removed=False)
            serializer = CollectionSerializer(collection, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Collection.DoesNotExist:
            return Response({"message": " collection does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryCreateView(APIView):
    """
        CategoryCreateView Class

        This view performs POST operation for collection object

        Parameters
        ----------
        APIView : rest_framework.views
    """

    permission_classes = [IsAdminUser, IsAuthenticated]

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={
            201: "CREATED",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
            HTTP POST request

            An HTTP endpoint that saves a Category object in DB

            Parameters
             ----------
            request : django.http.request

            Returns
            -------
            rest_framework.response
            returns success message if data saved successfully,error message otherwise
        """
        try:
            serializer = CategorySerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryManagementView(APIView):
    """
        CategoryManagementView Class

        This view performs PUT & Delete operation for collection object

        Parameters
        ----------
        APIView : rest_framework.views

    """

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """
            HTTP PUT request

            An HTTP endpoint that updates a category object for provided PK

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
            cata_obj = Category.objects.get(pk=pk)
            serializer = CategorySerializer(cata_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"message": "category does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def delete(self, request, pk, format=None):
        """
            HTTP DELETE request

            An HTTP endpoint that deletes a Category object for provided PK

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
            cata_obj = Category.objects.get(pk=pk)
            cata_obj.is_removed = True
            cata_obj.save()
            return Response({"message": "Category deleted Successfully"}, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return Response({"message": " category does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryView(APIView):
    """
        CategoryView Class

        This view performs GET operation for collection object

        Parameters
        ----------
        APIView : rest_framework.views
    """

    def get(self, request, pk):
        """
            HTTP GET request

            An HTTP endpoint that returns category object for provided PK

            Parameters
            ----------
            request : django.http.request

            pk : integer

            Returns
            ---------
            rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            cat_obj = Category.objects.get(pk=pk)
            serializer = CategorySerializer(cat_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"message": " Category does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryListView(APIView):
    """
        CategoryListView Class

        This view performs GET operation for collection object

        Parameters
        ----------
        APIView : rest_framework.views
    """

    def get(self, request):
        """
            HTTP GET request

            An HTTP endpoint that returns all Category objects

            Parameters
            ----------
            request : django.http.request

            Returns
            -------
            rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            cat_obj = Category.objects.filter(is_removed=False)
            serializer = CategorySerializer(cat_obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return Response({"message": "category does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FavouritesNftView(APIView):
    """
        FavouriteNFTList Class

        This view performs POST, GET & Delete operations on Favourite NFT object

        Parameters
        ----------
        APIView : rest_framework.views
    """

    @swagger_auto_schema(
        request_body=FavouriteNftSerializer,

        responses={
            201: "Created",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
            HTTP POST request

            An HTTP endpoint that saves a Favourite Item object in DB

            Parameters
            ----------
            request : django.http.request

            Returns
            -------
            rest_framework.response
            returns success message if data saved successfully,error message otherwise
        """
        try:
            serializer = FavouriteNftSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """
            HTTP GET request

            An HTTP endpoint that returns all Favourite Item objects

            Parameters
            ----------
            request : django.http.request

            Returns
            -------
            rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            favourite_nft = Nft.objects.filter(
                id__in=FavouriteNft.objects.filter(is_removed=False,
                                                   user=request.user.id
                                                   ).values_list('id')
            )
            serializer = FavouriteNftSerializer(favourite_nft, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except FavouriteNft.DoesNotExist:
            return Response({"message": "No Favourite NFTs"}, status=status.HTTP_400_BAD_REQUEST)


class FavouritesNFTDeleteView(APIView):
    """
        FavouritesNFTDeleteView Class

        This view performs Delete operation for favourites object

        Parameters
        ----------
        APIView : rest_framework.views
    """

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

            An HTTP endpoint that deletes a Favourite Item object for provided PK

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
            fav_obj = FavouriteNft.objects.get(pk=pk)
            fav_obj.is_removed = True
            fav_obj.save()
            return Response({"message": "Favorite NFT deleted"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportedNFTCreateView(APIView):
    """
        ReportedNFTCreateView Class

        This view performs POST operation for reported NFT object

        Parameters
        ----------
        APIView : rest_framework.views
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ReportedNftSerializer,

        responses={
            201: "CREATED",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
            HTTP POST request

            An HTTP endpoint that saves a reported NFT object in DB

            Parameters
            ----------
            request : django.http.request

            Returns
            -------
            rest_framework.response
            returns success message if data saved successfully,error message otherwise
        """
        try:
            data = request.data
            data['reporter'] = request.user.id
            serializer = ReportedNftSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportedNFTListView(APIView):
    """
        ReportedNFTListView Class

        This view performs GET operation for reported NFT object

        Parameters
        ----------
        APIView : rest_framework.views
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        """
            HTTP GET request

            An HTTP endpoint that returns all Reported NFT objects

            Parameters
            ----------
            request : django.http.request

            Returns
            -------
            rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            reported_nft_obj = ReportedNft.objects.filter(is_resolved=False, is_removed=False)
            serializer = ReportedNftSerializer(reported_nft_obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ReportedNft.DoesNotExist:
            return Response({"message": "category does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportedNFTView(APIView):
    """
        ReportedNFTView Class

        This view performs GET operation for collection object

        Parameters
        ----------
        APIView : rest_framework.views
    """

    def get(self, request, pk):
        """
            HTTP GET request

            An HTTP endpoint that returns reported NFT object for provided PK

            Parameters
            ----------
            request : django.http.request

            pk : integer

            Returns
            ---------
            rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            reported_nft_obj = ReportedNft.objects.get(pk=pk)
            serializer = ReportedNftSerializer(reported_nft_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ReportedNft.DoesNotExist:
            return Response({"message": " Category does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportedNFTDeleteView(APIView):
    """
        ReportedNFTDeleteView Class

        This view performs Delete operation for collection object

        Parameters
        ----------
        APIView : rest_framework.views
    """

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

            An HTTP endpoint that deletes a Reported NFT object for provided PK

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
            reported_nft = ReportedNft.objects.get(pk=pk)
            reported_nft.is_removed = True
            reported_nft.save()
            return Response({"message": "Reported NFT Deleted Successfully"}, status=status.HTTP_200_OK)

        except ReportedNft.DoesNotExist:
            return Response({"message": "Reported NFT does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def top_sellers(request):
    """
        Parameters: request
        ----------
        request: GET

        Returns: top sellers list
        -------

    """
    try:
        nft = Nft.objects.filter(is_removed=False).order_by('-price').annotate(user_name=F('owner__first_name'),
                                                                               profile_image=F(
                                                                                   'owner__user_profile__profile_image')).values(
            'user_name', 'profile_image')

        return Response({"top_sellers": nft}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def users_nft_data(request, id):
    """
        Parameters: request
        ----------
        request: GET

        Returns: user data object
        -------
    """
    try:

        user_data = Profile.objects.filter(
            is_removed=False,
            user_id=id).annotate(
            user_name=F(
                "user__first_name"),
            user_email=F('user__email'),
            nft_name=F('user__nft_owner__name'),
            nft_description=F(
                'user__nft_owner__description'),
            nft_image=F(
                'user__nft_owner__image'), ).values(
            'user_name',
            'user_email',
            'nft_name',
            'nft_description',
            'nft_image',
            'banner_image',
            'profile_image')

        return Response({"user_data": user_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

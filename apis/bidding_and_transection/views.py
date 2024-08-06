from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import BiddingSerializer, NftTranactionSerializer


class BiddingView(APIView):
    """BiddingView class

        This view performs GET operation for specific bid

         Parameters
        ----------
        APIView : rest_framework.views

    """

    def get(self, request, pk):
        """
        HTTP GET request

         A HTTP endpoint that returns Bid object for provided PK

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
            bid_obj = Bidding.objects.get(pk=pk)
            serializer = BiddingSerializer(bid_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Bidding.DoesNotExist:
            return Response({"message": "does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BiddingListView(APIView):
    """
    BiddingList class

        This view performs GET ,POST operation for Bidding Model

        Parameters
        ----------
        APIView : rest_framework.views

    """

    # permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        request_body=BiddingSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
        HTTP POST request

        A HTTP endpoint that saves a Bidding object  in DB


        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
             returns success message if data saved successfully,error message otherwise
        """
        try:
            serializer = BiddingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request, format=None):
        """
        HTTP GET request

             A HTTP endpoint that returns Bid object list

             Parameters
             ----------
             request : django.http.request

             Returns
             -------
             rest_framework.response
                 returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            bid = Bidding.objects.all()
            serializer = BiddingSerializer(bid, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NftTransactionView(APIView):
    """
        NftTransactionView class

        This view performs GET,POST operations for NftTransaction Model

        Parameters
        ----------
        APIView : rest_framework.views

    """

    @swagger_auto_schema(
        request_body=NftTranactionSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
        HTTP POST request

        A HTTP endpoint that saves a NftTransaction object  in DB


       Parameters
       ----------
       request : django.http.request

       Returns
       -------
       rest_framework.response
           returns success message if data saved successfully,error message otherwise
      """
        try:
            serializer = NftTranactionSerializer(data=request.data)
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

            A HTTP endpoint that returns NftTransaction object list

            Parameters
            ----------
            request : django.http.request

            Returns
            -------
            rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            trans_obj = NftTransaction.objects.all()
            serializer = NftTranactionSerializer(trans_obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NftTransactionDetail(APIView):

    def get(self, request, pk):
        """
         HTTP GET request

         A HTTP endpoint that returns NftTransaction object for provided PK

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
            trans_obj = NftTransaction.objects.get(pk=pk)
            serializer = NftTranactionSerializer(trans_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NftTransaction.DoesNotExist:
            return Response({"message": "Nft transaction detail doesn't exist against this id"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

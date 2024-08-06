from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import WalletSerializer


class WalletAPI(APIView):
    """
    Class for Wallet Management View
    """

    def get(self, request, pk):
        """
        Api for getting specific wallet information
        """
        try:
            wall_obj = Wallet.objects.get(pk=pk)
            serializer = WalletSerializer(wall_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({"message": "Wallet does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=WalletSerializer,

        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """
        Api for updating wallet information
        """
        try:
            wal_obj = Wallet.objects.get(pk=pk)
            serializer = WalletSerializer(wal_obj, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({"message": "Wallet does not exist"}, status=status.HTTP_400_BAD_REQUEST)

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
        Api for deleting wallet information
        """
        try:
            wall_obj = Wallet.objects.get(pk=pk)
            wall_obj.delete()
            return Response({"message": "Wallet deleted Successfully"}, status=status.HTTP_200_OK)

        except Wallet.DoesNotExist:
            return Response({"message": "Wallet does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletListView(APIView):
    """
    Class for Wallet List View
    """

    @swagger_auto_schema(
        request_body=WalletSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """
        Api for creating Wallet
        """
        try:
            serializer = WalletSerializer(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request):
        """
        Api for getting all wallet information
        """
        try:
            wallet_obj = Wallet.objects.all()
            serializer = WalletSerializer(wallet_obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

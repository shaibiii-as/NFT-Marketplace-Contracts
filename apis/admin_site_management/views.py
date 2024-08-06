from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class FAQView(APIView):
    """FAQView class

    This view performs GET,PUT, DELETE operations for FAQ Model

    Parameters
    ----------
    APIView : rest_framework.views

    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]

    def get(self, request, pk):
        """HTTP GET request

        A HTTP endpoint that returns FAQ object for provided PK

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
            faq_obj = FAQ.objects.get(pk=pk)
            serializer = FAQSerializer(faq_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FAQ.DoesNotExist:
            return Response(
                {"message": "FAQ does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=FAQSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """HTTP PUT request

        A HTTP endpoint that updates a FAQ object for provided PK

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
            faqs = FAQ.objects.get(pk=pk)
            serializer = FAQSerializer(instance=faqs, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(
                {"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def delete(self, request, pk):
        """HTTP DELETE request

        A HTTP endpoint that deletes a FAQ for provided PK

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
            faqs = FAQ.objects.get(pk=pk)
            faqs.is_active = False
            faqs.save()
            return Response(
                {"message": "FAQ deleted Successfully"}, status=status.HTTP_200_OK
            )
        except FAQ.DoesNotExist:
            return Response(
                {"message": "FAQ does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FAQListView(APIView):
    """FAQListView class

    This view performs POST and GET operations

    Parameters
    ----------
    APIView : rest_framework.views

    """

    # def get_permissions(self):
    #     if self.request.method == "POST":
    #         return [permissions.AllowAny()]
    #     else:
    #         return [permissions.IsAdminUser()]

    @swagger_auto_schema(
        request_body=FAQSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """HTTP POST request

        A HTTP endpoint that saves a FAQ object  in DB

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
            data["updated_by"] = request.user.id
            serializer = FAQSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        """HTTP GET request

        A HTTP endpoint that returns FAQ object list

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns HTTP 200 status if data returned successfully,error message otherwise
        """
        try:
            faqs = FAQ.objects.filter(is_active=True)
            serializer = FAQSerializer(faqs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FAQ.DoesNotExist:
            return Response(
                {"message": "FAQ does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ContactAPIView(APIView):
    """ContactView class

    This view performs POST and GET operations

    Parameters
    ----------
    APIView : rest_framework.views
    """

    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        """HTTP GET request

        A HTTP endpoint that returns Contacts object for provided PK

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
            con_obj = Contact.objects.get(pk=pk)
            serializer = FAQSerializer(con_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FAQ.DoesNotExist:
            return Response(
                {"message": "contact does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=ContactSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def put(self, request, pk):
        """HTTP PUT request

        A HTTP endpoint that updates a Contacts object for provided PK

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
            contact = Contact.objects.get(pk=pk)
            serializer = ContactSerializer(contact, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Contact.DoesNotExist:
            return Response(
                {"message": "Contact does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def delete(self, request, pk):
        """HTTP DELETE request

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
            contact = Contact.objects.get(pk=pk)
            contact.is_removed = True
            contact.save()
            return Response(
                {"message": "Contact deleted Successfully"}, status=status.HTTP_200_OK
            )
        except Contact.DoesNotExist:
            return Response(
                {"message": "Contact does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ContactListView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAdminUser()]
        else:
            return [permissions.AllowAny()]

    @swagger_auto_schema(
        request_body=ContactSerializer,
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        """HTTP POST request

        A HTTP endpoint that saves a Contacts object  in DB


        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response
            returns success message if data saved successfully,error message otherwise
        """
        try:
            # data = request.data
            # data['resolved_by'] = request.user.id
            # print(request.user.id)
            serializer = ContactSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        """HTTP GET request

        A HTTP endpoint that returns Contacts objects list

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
            contact = Contact.objects.filter(is_removed=False)
            serializer = ContactSerializer(contact, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Contact.DoesNotExist:
            return Response(
                {"message": "Contact does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

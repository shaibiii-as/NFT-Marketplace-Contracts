from apis.user_management.serializers import UserSerializer
from rest_framework.serializers import ModelSerializer

from .models import *


class CategorySerializer(ModelSerializer):
    """
    Serializer for Category
    """

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ("is_removed", "is_active")


class NFTSerializer(ModelSerializer):
    """
    Serializer for NFT
    """

    class Meta:
        model = Nft
        fields = '__all__'
        read_only_fields = (
            "is_hidden", "is_put_on_sale", "updated_at", "is_removed", "created_at", 'total_views', 'sale_type')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['collection'] = f"{instance.collection.name}"
        response['owner'] = f"{instance.owner.first_name} {instance.owner.last_name}"
        return response


class CollectionUserSerializer(ModelSerializer):
    """
    Serializer for  Collection
    """

    owner = UserSerializer()

    class Meta:
        model = Collection
        fields = "__all__"
        depth = 2


class FavouriteNftSerializer(ModelSerializer):
    """
    Serializer for Favourite NFTs
    """

    class Meta:
        model = FavouriteNft
        fields = "__all__"
        read_only_fields = ("is_removed", "date")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["nft"] = f"{instance.nft.name}"
        response["user"] = f"{instance.user.first_name} {instance.user.last_name}"
        return response


class ReportedNftSerializer(ModelSerializer):
    """
    Serializer for Reported NFTs
    """

    class Meta:
        model = ReportedNft
        fields = "__all__"
        read_only_fields = ("is_resolved",)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["nft"] = f"{instance.nft.name}"
        response[
            "reporter"
        ] = f"{instance.reporter.first_name} {instance.reporter.last_name}"
        return response


class CollectionSerializer(ModelSerializer):
    """
    Serializer for Collection
    """

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ("is_removed", "created_at", "updated_at")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["category"] = f"{instance.category.name}"
        response["user"] = f"{instance.user.first_name} {instance.user.last_name}"
        return response

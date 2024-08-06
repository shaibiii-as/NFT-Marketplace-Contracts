from django_filters import FilterSet, DateFilter
from apis.nft_management.models import Collection, Category, FavouriteNft, ReportedNft, NftPriceHistory, Nft


class CollectionFilter(FilterSet):

    class Meta:
        model = Collection
        fields = ['name', 'category', 'user', 'is_removed']


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = ['name', 'is_active', 'is_removed']


class FavouriteNftFilter(FilterSet):
    class Meta:
        model = FavouriteNft
        fields = ['user', 'nft', 'is_favorite']


class ReportedNftFilter(FilterSet):
    class Meta:
        model = ReportedNft
        fields = ['nft', 'reporter', 'report_type','is_resolved']


class nphFilter(FilterSet):
    class Meta:
        model = NftPriceHistory
        fields = ['nft']


class nftFilter(FilterSet):
    class Meta:
        model = Nft
        fields = ['name']

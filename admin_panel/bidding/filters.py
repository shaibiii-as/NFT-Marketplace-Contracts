import django_filters
from apis.bidding_and_transection.models import Bidding, NftTransaction
from django_filters import DateFilter


class BiddingFilter(django_filters.FilterSet):
    """
    Filters for Bidding
    """

    class Meta:
        model = Bidding
        fields = ['price']


class BiddingTransactionFilter(django_filters.FilterSet):
    """
    Filters for Bidding Transaction
    """
    start_date = DateFilter(field_name="sold_date", lookup_expr="gte")

    class Meta:
        model = NftTransaction
        fields = ['buyer']
        exclude = ['sold_date']

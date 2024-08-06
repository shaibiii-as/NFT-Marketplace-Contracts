import django_filters
from apis.wallet_management.models import Wallet, WalletTransaction


class WalletFilter(django_filters.FilterSet):
    class Meta:
        model = Wallet
        fields = ['user']



class WalletTransactionFilter(django_filters.FilterSet):
    class Meta:
        model = WalletTransaction
        fields = ['transaction_type']
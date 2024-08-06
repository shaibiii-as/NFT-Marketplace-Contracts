from django.urls import path
from . import views

app_name = 'wallet_manager'

urlpatterns = [
    path('wallet_transaction/', views.WalletTransactiondetailView.as_view(), name='wallet-transaction'),
    path('wallet/', views.WalletDisplay.as_view(), name='wallet'),
    path('wallet/<int:id>', views.DeleteWalletView.as_view(), name='wallet-delete'),
]

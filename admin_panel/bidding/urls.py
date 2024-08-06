from django.urls import path
from . import views

app_name = 'bidding'

urlpatterns = [
    path('bidding/', views.BiddingdetailView.as_view(), name='bidding-list'),
    path('bidding/delete/<int:id>', views.DeleteBiddingView.as_view(), name='bidding-delete'),
    path('nft_transaction/', views.TransactiondetailView.as_view(), name='Nft-transaction-list'),
    path('nft_transaction/delete/<int:id>', views.DeleteTransactionView.as_view(), name='transaction-delete'),
]

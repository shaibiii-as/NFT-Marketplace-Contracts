from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.edit import DeleteView
from django.views import View
from .filters import WalletFilter, WalletTransactionFilter
from apis.wallet_management.models import Wallet, WalletTransaction
from django.core.paginator import Paginator


class WalletTransactiondetailView(View):
    def get(self, request):
        walletTransaction = WalletTransaction.objects.all().order_by('id')
        walletTransaction_count=walletTransaction.count()
        myfilter = WalletTransactionFilter(request.GET, queryset=walletTransaction)
        wallettransaction = myfilter.qs
        p = Paginator(wallettransaction.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'wallet_transaction_index.html',
                      {'wallet_transactions': wallettransaction, 'myfilter': myfilter, 'obj': obj,'walletTransaction_count':walletTransaction_count})


class WalletDisplay(View):
    def get(self, request):
        wallet = Wallet.objects.all().order_by('id')
        wallet_count = wallet.count()
        myfilter = WalletFilter(request.GET, queryset=wallet)
        wallet = myfilter.qs
        p = Paginator(wallet.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'index.html', {'wallets': wallet, 'myfilter': myfilter, 'obj': obj,'wallet_count':wallet_count})


class DeleteWalletView(DeleteView):
    def get(self, request, id):
        """
        Http get request use to Render list collection template after delete the collection.

        *Template:*

        `template:` collection_app/list-collection.html

        *Returns:*

        `HttpResponseRedirect:` collection list template

        """
        object = Wallet.objects.get(id=id)
        object.is_removed = True
        object.save()
        url = reverse('wallet_manager:wallet')
        return HttpResponseRedirect(url)

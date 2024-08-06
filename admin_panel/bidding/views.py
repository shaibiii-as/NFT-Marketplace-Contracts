from apis.bidding_and_transection.models import Bidding, NftTransaction
from django.core.paginator import Paginator
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views import View
from django.views.generic.edit import DeleteView

from .filters import BiddingFilter, BiddingTransactionFilter


class BiddingdetailView(View):
    """
        *ListUerView class*

        This view used to perform get request on user object to view the list of user object

        *Parameters*

        `View:`  django.views

        """

    def get(self, request):
        """
        Http get request use to Render create_collection template, categories and users.

        *Template:*

        `template:` collection_app/list-collection.html

        *Returns:*

        `render:` list-collection template and collection list

        """
        bidding_list = Bidding.objects.all().order_by('id')
        bidding_count = bidding_list.count()
        myfilter = BiddingFilter(request.GET, queryset=bidding_list)
        bidding = myfilter.qs
        p = Paginator(bidding.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'bidding_index.html',
                      {'biddings': bidding, 'myfilter': myfilter, 'obj': obj, 'bidding_count': bidding_count})


class DeleteBiddingView(View):
    """
    View for deleting bid
    """

    def get(self, request, id):
        object = Bidding.objects.get(id=id)
        object.status = False
        object.save()
        url = reverse('bidding:bidding-list')
        return HttpResponseRedirect(url)


class TransactiondetailView(View):
    """
    view for transaction detail
    """

    def get(self, request):
        Transaction = NftTransaction.objects.all().order_by('id')
        Transaction_count = Transaction.count()
        myfilter = BiddingTransactionFilter(request.GET, queryset=Transaction)
        transaction = myfilter.qs
        p = Paginator(transaction.order_by('id'), 5)
        page = request.GET.get('page')
        obj = p.get_page(page)
        return render(request, 'nft_transaction_index.html',
                      {'transaction': transaction, 'myfilter': myfilter, 'obj': obj,
                       'Transaction_count': Transaction_count})


class DeleteTransactionView(DeleteView):
    """
    View for Delete Transaction View
    """

    def get(self, request, id):
        object = NftTransaction.objects.get(id=id)
        object.is_removed = True
        object.save()
        url = reverse('bidding:Nft-transaction-list')
        return HttpResponseRedirect(url)

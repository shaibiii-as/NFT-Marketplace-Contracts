from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy


class UserRestrictionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        paths = [
            '/admin_site/dashboard/',
            '/admin_site/home/',
            '/admin_site/profiles/',
            '/admin_site/bidding/',
            '/admin_site/nft_transaction/',
            '/admin_site/list_collection/',
            '/admin_site/list_category/',
            '/admin_site/create_category/',
            '/admin_site/update_category/',
            '/admin_site/list_favorites_nft/',
            '/admin_site/nfts_create/',
            '/admin_site/nftprice-list/',
            '/admin_site/list_faq/',
            '/admin_site/wallet_transaction/',
            '/admin_site/wallet/',
            '/admin_site/list_contact/',
        ]

        if str(user) != 'AnonymousUser' or not (request.path.strip() in paths):
            response = self.get_response(request)
            return response
        else:
            return HttpResponseRedirect('/admin_site/login')


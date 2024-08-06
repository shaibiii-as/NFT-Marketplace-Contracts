from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

app_name = "nft_management"

urlpatterns = [
    path("list_collection/", views.ListCollectionView.as_view(), name='list-collection'),
    path("delete_collection/<int:id>/", views.DeleteCollectionView.as_view(), name='delete-collection'),
    path("list_category/", views.ListCategoryView.as_view(), name='list-category'),
    path("create_category/", views.CreateCategoryView.as_view(), name='create-category'),
    path("update_category/<int:id>/", views.UpdateCategoryView.as_view(), name='update-category'),
    path("delete_category/<int:id>/", views.DeleteCategoryView.as_view(), name='delete-category'),
    path("list_favorites_nft/", views.ListFavoritesNFTView.as_view(), name='list-favorites-nft'),
    path("delete_favorites_nft/<int:id>/", views.DeleteFavoritesNFTView.as_view(), name='delete-favorites-nft'),
    path("list_reported_nft/", views.ListReportedNFTView.as_view(), name='list-reported-nft'),
    path("resolve_reported_nft/<int:id>/", views.ResolveReportedNFTView.as_view(), name='resolve-reported-nft'),
    path("list_collection/", views.ListCollectionView.as_view(), name='list-collection'),
    path("delete_collection/<int:id>", views.DeleteCollectionView.as_view(), name='delete-collection'),
    path("nfts_list/", views.NftListDisplay.as_view(), name="nfts_list"),
    path("nfts_update/<int:pk>/", views.NftUpdate.as_view(), name="nfts_update"),
    path("nfts_delete/<int:pk>/", views.NftDelete.as_view(), name="nfts_delete"),
    path("nfts_create/", views.NftCreate.as_view(), name="nfts_create"),
    # NftPrice History
    path("nftprice_histroy-add/",views.AddNftPriceHistory.as_view(),name="add-price-history"),
    path(
        "nftprice_histroy-delete/<int:pk>",
        views.DeletePriceHistory.as_view(),
        name="price-history-delete",
    ),
    path("nftprice-list/", views.PriceHistoryList.as_view(), name="price-history-list"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

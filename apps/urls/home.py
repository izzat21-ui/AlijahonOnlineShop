from django.urls import path
from apps.views import HomeListView, WishlistView, ProductListView, \
    LikeListView, ProductDetailView, CompetitionListView

urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("wishlist/<int:product_id>", WishlistView.as_view(), name="product-list"),
    path("products/<str:slug>", ProductListView.as_view(), name="product-list"),
    path("wishlist", LikeListView.as_view(), name="wish-list"),
    path("product/detail/<str:slug>", ProductDetailView.as_view(), name="product-detail"),
    path("competition", CompetitionListView.as_view(), name="competition"),
]

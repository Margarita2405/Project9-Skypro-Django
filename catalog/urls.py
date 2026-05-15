from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (CategoryProductsView, ContactsView, HomeView, ProductCreateView, ProductDeleteView,
                           ProductDetailView, ProductListView, ProductUpdateView, UnpublishProductView)

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/detail/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("products/delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("product/unpublish/<int:pk>/", UnpublishProductView.as_view(), name="unpublish_product"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("category/<int:category_id>/", CategoryProductsView.as_view(), name="category_products"),
]

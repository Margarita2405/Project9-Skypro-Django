from django.urls import path
from catalog.views import (
    HomeView, ProductListView, ProductDetailView,
    ContactsView, CategoryProductsView
)
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
]

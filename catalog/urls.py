from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    # Главная страница (презентационная)
    path("", views.home, name="home"),
    # Каталог товаров
    path("catalog/", views.product_list, name="product_list"),
    path("catalog/<int:pk>/", views.product_detail, name="product_detail"),
    # Категории
    path("catalog/category/<int:category_id>/", views.category_products, name="category_products"),
    # Контакты
    path("contacts/", views.contacts, name="contacts"),
]

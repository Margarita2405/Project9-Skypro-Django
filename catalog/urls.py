from django.urls import path
from catalog.apps import CatalogConfig
from catalog import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.contacts, name='contacts'),
]
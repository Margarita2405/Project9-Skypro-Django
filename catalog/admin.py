from django.contrib import admin

from catalog.models import Category, Contact, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "is_published", "owner",)
    list_filter = ("category", "is_published", "owner",)
    search_fields = (
        "name",
        "description",
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone")
    list_filter = ("name",)
    search_fields = (
        "name",
        "phone",
    )

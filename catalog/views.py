from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Category, Contact, Product


def home(request: HttpRequest) -> HttpResponse:
    """Главная презентационная страница"""
    # Получаем последние 6 товаров для показа на главной
    latest_products = Product.objects.select_related("category").all().order_by("-created_at")[:6]

    # Получаем категории для отображения
    categories = Category.objects.all()

    context = {
        "latest_products": latest_products,
        "categories": categories,
        "title": "Skystore - Магазин электроники и не только",
    }
    return render(request, "catalog/home.html", context)


def product_list(request: HttpRequest) -> HttpResponse:
    """Страница каталога со списком всех товаров"""
    products = Product.objects.select_related("category").all().order_by("-created_at")
    categories = Category.objects.all()

    context = {
        "products": products,
        "categories": categories,
        "title": "Каталог товаров",
    }
    return render(request, "catalog/product_list.html", context)


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Детальная страница товара"""
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    context = {
        "product": product,
        "title": product.name,
    }
    return render(request, "catalog/product_detail.html", context)


def contacts(request: HttpRequest) -> HttpResponse:
    """Страница контактов"""
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if name and phone:
            Contact.objects.create(name=name, phone=phone, message=message)
            messages.success(request, f"Спасибо {name}! Ваше сообщение отправлено.")
            return redirect("catalog:contacts")
        else:
            messages.error(request, "Пожалуйста, заполните имя и телефон.")

    contacts_list = Contact.objects.all().order_by("-created_at")[:5]

    context = {
        "contacts": contacts_list,
        "title": "Контакты",
    }
    return render(request, "catalog/contacts.html", context)


def category_products(request, category_id):
    """Товары по категории"""
    category = get_object_or_404(Category, pk=category_id)
    products = category.products.all().order_by("-created_at")
    categories = Category.objects.all()

    context = {
        "category": category,
        "products": products,
        "categories": categories,
        "title": f"Категория: {category.name}",
    }
    return render(request, "catalog/product_list.html", context)

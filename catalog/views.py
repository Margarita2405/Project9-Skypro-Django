from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from catalog.models import Category, Contact, Product


def home(request: HttpRequest) -> HttpResponse:
    # Получаем последние 5 созданных продуктов (по дате создания)
    latest_products = Product.objects.order_by("-created_at")[:5]

    # Выводим в консоль
    print("=" * 50)
    print("Последние 5 созданных продуктов:")
    print("=" * 50)
    for i, product in enumerate(latest_products, 1):
        print(f"{i}. {product.name} - {product.price} руб.")
        print(f"   Категория: {product.category.name}")
        print(f"   Дата создания: {product.created_at}")
        print("-" * 30)

    # Получаем все категории для отображения
    categories = Category.objects.all()

    context = {
        "latest_products": latest_products,
        "categories": categories,
    }

    return render(request, "home.html", context)


def contacts(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # Отладка - посмотрите, что приходит
        print("POST данные:", request.POST)

        # Получение данных из формы
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        print(f"Получено: name={name}, phone={phone}, message={message}")

        if name and phone:  # Проверка, что данные есть
            contact = Contact.objects.create(name=name, phone=phone, message=message)
            print(f"Сохранен контакт ID: {contact.id}")
            return HttpResponse(f"Спасибо {name}! Ваше сообщение получено.")
        else:
            print("Ошибка: не все поля заполнены")
            return HttpResponse("Пожалуйста, заполните все поля.")

    # GET запрос - получаем все контакты из БД для отображения
    contacts_list = Contact.objects.all().order_by("-created_at")

    # Выводим в консоль для проверки
    print("=" * 40)
    print("Сохраненные контакты:")
    for contact in contacts_list:
        print(f"Имя: {contact.name}, Телефон: {contact.phone}")
        print(f"Сообщение: {contact.message[:100] if contact.message else 'Нет сообщения'}")
        print("-" * 30)

    context = {
        "contacts": contacts_list,
    }

    return render(request, "contacts.html", context)

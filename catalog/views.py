from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, DetailView, View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from catalog.models import Category, Contact, Product


class HomeView(TemplateView):
    template_name = "catalog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_products"] = Product.objects.select_related("category").order_by("-created_at")[:6]
        context["categories"] = Category.objects.all()
        context["title"] = "Skystore - Качественные товары для дома и офиса"
        return context


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    ordering = "-created_at"

    def get_queryset(self):
        # select_related для оптимизации
        return super().get_queryset().select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["title"] = "Каталог товаров"
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return super().get_queryset().select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context

class ContactsView(View):
    template_name = "catalog/contacts.html"

    def get(self, request):
        contacts_list = Contact.objects.all().order_by("-created_at")[:5]
        context = {
            "contacts": contacts_list,
            "title": "Контакты",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if name and phone:
            Contact.objects.create(name=name, phone=phone, message=message)
            messages.success(request, f"Спасибо {name}! Ваше сообщение отправлено.")
            return HttpResponseRedirect(reverse_lazy("catalog:contacts"))
        else:
            messages.error(request, "Пожалуйста, заполните имя и телефон.")
            # При ошибке возвращаем ту же страницу с уже отправленными данными
            contacts_list = Contact.objects.all().order_by("-created_at")[:5]
            context = {
                "contacts": contacts_list,
                "title": "Контакты",
            }
            return render(request, self.template_name, context)


class CategoryProductsView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    ordering = "-created_at"

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        self.category = get_object_or_404(Category, pk=category_id)
        return self.category.products.all().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["category"] = self.category
        context["title"] = f"Категория: {self.category.name}"
        return context

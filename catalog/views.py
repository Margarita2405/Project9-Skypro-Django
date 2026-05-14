from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View

from catalog.models import Category, Contact, Product

from .forms import ProductForm


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
        context['request'] = self.request
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.owner != self.request.user:
            raise PermissionDenied("Редактировать может только владелец")
        return object


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.owner != self.request.user and not self.request.user.has_perm('catalog.delete_product'):
            raise PermissionDenied("Удалять может владелец или модератор")
        return object


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.has_perm('catalog.can_unpublish_product'):
            raise PermissionDenied("Нет права отменять публикацию")
        product.is_published = False
        product.save()
        return redirect('catalog:product_detail', pk=pk)


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
        context['request'] = self.request
        context["categories"] = Category.objects.all()
        context["category"] = self.category
        context["title"] = f"Категория: {self.category.name}"
        return context

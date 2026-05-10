import os

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from PIL import Image

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]

    FORBIDDEN_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите наименование товара"}
        )

        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите описание товара"}
        )

        self.fields["image"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Загрузите изображение товара"}
        )

        self.fields["category"].widget.attrs.update(
            {"class": "form-select", "placeholder": "Выберите категорию товара"}
        )

        self.fields["price"].widget.attrs.update({"class": "form-control", "placeholder": "Укажите цену товара"})

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Цена продукта не может быть отрицательной.")
        return price

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            name_lower = name.lower()
            for word in self.FORBIDDEN_WORDS:
                if word in name_lower:
                    raise ValidationError(f'Название не должно содержать слово "{word}".')
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description:
            desc_lower = description.lower()
            for word in self.FORBIDDEN_WORDS:
                if word in desc_lower:
                    raise ValidationError(f'Описание не должно содержать слово "{word}".')
        return description

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            # Проверка размера (5 МБ = 5 * 1024 * 1024 байт)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError(_("Размер файла не должен превышать 5 МБ."))

            ext = os.path.splitext(image.name)[1].lower()
            if ext not in (".jpg", ".jpeg", ".png"):
                raise ValidationError("Поддерживаются только форматы JPEG и PNG.")

            try:
                img = Image.open(image)
                if img.format not in ("JPEG", "PNG"):
                    raise ValidationError("Файл не является изображением JPEG или PNG.")
            except Exception:
                raise ValidationError("Файл повреждён или не является изображением.")
        return image

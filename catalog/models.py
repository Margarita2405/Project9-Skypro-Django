from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Наименование категории", help_text="Введите наименование категории"
    )
    description = models.TextField(
        verbose_name="Описание категории", help_text="Введите описание категории", blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Наименование товара", help_text="Введите наименование товара"
    )
    description = models.TextField(
        verbose_name="Описание товара", help_text="Введите описание товара", blank=True, null=True
    )
    image = models.ImageField(upload_to="images/", blank=True, null=True, verbose_name="Изображение товара")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория товара",
        help_text="Введите название категории",
        blank=False,
        related_name="products",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за покупку",
        help_text="Указывайте цену в рублях с учетом НДС",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name", "category"]


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя", help_text="Введите ваше имя")
    phone = models.CharField(max_length=20, verbose_name="Контактный телефон", help_text="Введите номер телефона")
    message = models.TextField(verbose_name="Сообщение", help_text="Введите ваше сообщение", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self) -> str:
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["-created_at"]

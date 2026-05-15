from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке пользователей
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'country', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'country')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)

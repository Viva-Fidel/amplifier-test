from django.contrib import admin

from .models import Category, Material


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "parent")
    search_fields = ("name", "code")
    list_filter = ("parent",)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "code", "cost")
    search_fields = ("name", "code")
    list_filter = ("category",)

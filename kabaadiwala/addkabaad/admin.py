from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','image',	'description','price','decision']
    list_filter = ['decision', 'created', 'updated']
    list_editable = ['price', 'decision']
    prepopulated_fields = {'slug': ('name',)}
from django.contrib import admin
from shop.models import Category, Products

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
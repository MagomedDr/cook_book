from django.contrib import admin
from .models import Product, Recipe, RecipeProduct

class RecipeProductInline(admin.TabularInline):
    model = RecipeProduct

class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeProductInline,)

admin.site.register(Product)
admin.site.register(Recipe, RecipeAdmin)
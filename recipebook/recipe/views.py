from django.shortcuts import render
from django.http import JsonResponse
from .models import Recipe, Product, RecipeProduct

def add_product_to_recipe(request):
    if request.method == 'GET':
        try:
            recipe_id = request.GET.get('recipe_id')
            product_id = request.GET.get('product_id')
            weight = request.GET.get('weight')

            recipe = Recipe.objects.get(pk=recipe_id)
            product = Product.objects.get(pk=product_id)

            recipeproduct, created = RecipeProduct.objects.get_or_create(recipe=recipe, product=product)
            recipeproduct.weight_in_grams = weight
            recipeproduct.save()

            return JsonResponse({'message': 'Product added/updated successfully.'})
        except (ValueError, Recipe.DoesNotExist, Product.DoesNotExist) as e:
            return JsonResponse({'error': str(e)}, status=400)

def cook_recipe(request):
    if request.method == 'GET':
        try:
            recipe_id = request.GET.get('recipe_id')
            recipe = Recipe.objects.get(pk=recipe_id)

            recipe_products = RecipeProduct.objects.filter(recipe=recipe)          
            for recipe_product in recipe_products:
                recipe_product.product.times_used += 1
                recipe_product.product.save()

            return JsonResponse({'message': 'Recipe cooked successfully.'})
        except (ValueError, Recipe.DoesNotExist, Product.DoesNotExist) as e:
            return JsonResponse({'error': str(e)}, status=400)

def show_recipes_without_product(request, product_id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(pk=product_id)
            recipes_without_product = Recipe.objects.exclude(recipeproduct__product=product)
            recipes_less_than_10g = Recipe.objects.filter(recipeproduct__product=product, recipeproduct__weight_in_grams__lt=10)

            context = {
                'product': product,
                'recipes_without_product': recipes_without_product,
                'recipes_less_than_10g': recipes_less_than_10g,
            }

            return render(request, 'recipes_without_product.html', context)
        except Product.DoesNotExist:
            return render(request, 'error.html', {'error_message': 'Product does not exist.'})
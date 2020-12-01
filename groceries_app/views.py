from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from groceries_app.models import Meal, IngredientQuantity, Measurement



class HomeView(TemplateView):
    template_name = 'home.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class MealChoiceView(TemplateView):
    template_name = 'grocery_planner/gp1-meal-choice.html'

    def convert_to_tsp(self, measurement, quantity):
        if measurement == 'tbsp':
            quantity *= 3
        elif measurement == 'cup':
            quantity *= 48
        return quantity

    def check_tsp(self, quantity):
        measurement = 'tsp'
        if quantity >= 48:
            measurement = 'cup'
            quantity = quantity / 48
        elif quantity >= 3:
            measurement = 'tbsp'
            quantity = quantity / 3
        return measurement, quantity

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal_list'] = Meal.objects.order_by('name')
        return context

    def post(self, request):
        all_ingredients = {}
        meals = request.POST
        for meal, batch_size in meals.items():
            if meal == 'csrfmiddlewaretoken':
                pass
            elif batch_size == '0':
                pass
            else:
                meal_id = Meal.objects.get(name=meal)
                ingredients = IngredientQuantity.objects.all().filter(meal_name=meal_id.id)
                for ingredient in ingredients:
                    # prep ingredient variables
                    quantity = ingredient.quantity * int(batch_size)
                    measurement = str(ingredient.measurement.measurement)
                    ingredient = str(ingredient.ingredient)
                    if measurement == 'cup' or measurement == 'tbsp':
                        quantity = self.convert_to_tsp(measurement, quantity)
                        measurement = 'tsp'
                    elif measurement == 'splash' or measurement == 'pinch':
                        measurement = 'to taste'

                    # add ingredient to all_ingredients
                    if ingredient not in all_ingredients:
                        all_ingredients[ingredient] = {measurement: quantity}
                    elif measurement in all_ingredients[ingredient]:
                        all_ingredients[ingredient][measurement] += quantity
                    else:
                        all_ingredients[ingredient][measurement] = quantity

        # normalize tsp, tbsp, cups
        for ingredient, measurements in all_ingredients.items():
            if 'tsp' in measurements:
                quantity = measurements['tsp']
                measurement, quantity = self.check_tsp(quantity)
                if measurement != 'tsp':
                    measurements[measurement] = quantity
                    del measurements['tsp']

        request.session['ingredients'] = all_ingredients
        return redirect('ingredient-plan')


class IngredientPlanView(TemplateView):    
    def get(self, request):
        all_ingredients = request.session.get('ingredients')
        measurements = Measurement.objects.all()
        return render(
            request,
            'grocery_planner/gp2-ingredient-list.html',
            {'ingredients': all_ingredients,
             'all_measurements': measurements}
        )

    def post(self, request):
        ingredients = request.POST
        print(ingredients)
        return HttpResponse(ingredients)


class RecipeListView(ListView):
    template_name = 'recipes/recipes_list.html'
    model = Meal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal_list'] = Meal.objects.order_by('name')
        return context


class RecipeDetailView(DetailView):
    template_name = 'recipes/recipes_detail.html'
    model = Meal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredient_list'] = IngredientQuantity.objects.filter(
            meal_name=context['meal'])
        return context

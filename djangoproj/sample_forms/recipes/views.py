from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from recipes.models import Recipe, RecipeIngredient
from recipes.forms import UserSubmittedRecipeForm, IngredientFormSet

def submit_recipe(request):
    if request.POST:
        form = UserSubmittedRecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            ingredient_formset = IngredientFormSet(request.POST, instance=recipe)
            if ingredient_formset.is_valid():
                recipe.save()
                ingredient_formset.save()
                return HttpResponseRedirect(reverse('recipes:recipes_submit_posted'))
    else:
        form = UserSubmittedRecipeForm()
        ingredient_formset = IngredientFormSet(instance=Recipe())
    return render(request, "recipes/submit.html", {
        "form": form,
        "ingredient_formset": ingredient_formset}
    )


def recipe_posted(request):
    return HttpResponse("Recept je bil dodan v bazo")


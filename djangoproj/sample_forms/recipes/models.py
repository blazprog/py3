from django.db import models

class Recipe(models.Model):
    pubdate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    instructions = models.TextField()

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.CharField(max_length=200)

    def __str__(self):
        return self.ingredient





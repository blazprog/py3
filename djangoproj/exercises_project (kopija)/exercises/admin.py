from django.contrib import admin

from django.contrib import admin
from .models import Language, Subject, ExercisesModel

admin.site.register(Language)
admin.site.register(Subject)
admin.site.register(ExercisesModel)

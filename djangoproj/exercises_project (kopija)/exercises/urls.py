from django.conf.urls import patterns, include, url
from .views import (ExerciseDetailView, ExercisesListView, ExerciseCreateView, ExerciseUpdateView,
                    ExerciseSolveView, SampleFormView,SelectLanguageView)


urlpatterns = patterns('',
     #url(r'^$', MyView.as_view(), name='index'),
     url(r'^select_language$', SelectLanguageView.as_view(), name='select_language'),
     url(r'^(?P<language>\w\w)/(?P<pk>\d+)$', ExercisesListView.as_view(), name='exercise_list'),
     url(r'^(?P<language>\w\w)$', ExercisesListView.as_view(), name='exercise_list'),
     url(r'^exercise/(?P<language>\w\w)/(?P<pk>[-_\d]+)$', ExerciseDetailView.as_view(), name='exercise_detail'),
     url(r'^exercise_update/(?P<language>\w\w)/(?P<pk>[-_\d]+)$', ExerciseUpdateView.as_view(), name='exercise_update'),
     url(r'^exercise_solve/(?P<language>\w\w)/(?P<pk>[-_\d]+)$', ExerciseSolveView.as_view(), name='exercise_solve'),
     url(r'^exercise_create/(?P<language>\w\w)/(?P<subject>\d+)$', ExerciseCreateView.as_view(), name='exercise_create'),
     url(r'^sample_form$', SampleFormView.as_view(), name='sample_form'),
     )
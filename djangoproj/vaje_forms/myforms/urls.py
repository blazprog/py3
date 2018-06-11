__author__ = 'blazko'

from django.conf.urls import patterns, include, url
from .views import (SubjectCreateView,SubjectUpdateView,SubjectList,GroupedSubjects,
                    ExerciseList,ExerciseUpdateView,ExerciseCreateView,ExerciseSolveView,ExerciseView,
                    LanguageList, LanguageUpdateView,LanguageCreateView,
                    register,LoginView, user_logout)


urlpatterns = patterns('',
       url(r"^subjects/(?P<language>\w\w)$",GroupedSubjects.as_view(), name="subjects"),

       url(r"^exercises/(?P<language>\w\w)/(?P<subject>\d+)/$",ExerciseList.as_view(), name="exercises"),
       url(r"^exercise_edit/(?P<language>\w\w)/(?P<pk>\d+)/$",ExerciseUpdateView.as_view(), name="exercise_edit"),
       url(r"^exercise_solve/(?P<language>\w\w)/(?P<pk>\d+)/$",ExerciseSolveView.as_view(), name="exercise_solve"),
       url(r"^exercise_add/(?P<language>\w\w)$",ExerciseCreateView.as_view(), name="exercise_add"),
       url(r"^exercise2_add/(?P<language>\w\w)$",ExerciseView.as_view(), name="exercise_add2"),

       url(r"^subjects_list/(?P<language>\w\w)$",SubjectList.as_view(), name="subjects_list"),
       url(r"^subject_add/(?P<language>\w\w)$",SubjectCreateView.as_view(), name="subject_add"),
       url(r"^subject_edit/(?P<language>\w\w)/(?P<pk>\d+)$",SubjectUpdateView.as_view(), name="subject_edit"),

       url(r"^language_list/(?P<language>\w\w)$",LanguageList.as_view(), name="language_list"),
       url(r"^language_add/(?P<language>\w\w)$",LanguageCreateView.as_view(), name="language_add"),
       url(r"^language_edit/(?P<language>\w\w)/(?P<pk>\d+)$",LanguageUpdateView.as_view(), name="language_edit"),

       url(r"^register/(?P<language>\w\w)$",register, name="register"),
       url(r"^login/(?P<language>\w\w)$",LoginView.as_view(), name="login"),
       url(r"^logout/(?P<language>\w\w)$",user_logout, name="logout"),
       )
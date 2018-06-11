from django.conf.urls import patterns, url
from  recipes import views


urlpatterns = patterns('',
    url(r'^$', views.submit_recipe, name='new_recipe'),
    url(r'^recipe_submitted$', views.recipe_posted, name='recipes_submit_posted'),
)

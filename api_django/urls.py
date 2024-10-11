from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('users/',views.get_users,name='get_all_users'),
   path('courses/',views.get_courses,name='get_all_courses'),
   path('areas/',views.get_areas,name='get_all_areas'),
   path('organizations/',views.get_organizations,name='get_all_organizations'),
   path('data',views.user_manager),
]
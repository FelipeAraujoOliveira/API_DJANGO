from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('users/',views.user_manager),
   path('register/',views.register,name="register"),
   path('login/',views.login, name="login"),
   path('courses/',views.course_manager),
   path('areas/',views.area_manager),
   path('organizations/',views.organization_manager),
]
from django.contrib import admin
from django.urls import path
from .views import user_views,area_views,course_views,organization_views

urlpatterns = [
   path('users/',user_views.user_manager),
   path('register/',user_views.register,name="register"),
   path('login/',user_views.login, name="login"),
   path('courses/',course_views.course_manager),
   path('areas/',area_views.area_manager),
   path('organizations/',organization_views.organization_manager),
   path('email/',user_views.send_verification_email)
]
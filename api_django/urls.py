from django.contrib import admin
from django.urls import path
from .views import user_views,area_views,course_views,organization_views
from .views.user_views import UserTemplate

urlpatterns = [
   path('users/',user_views.UserManager.as_view()),
   path('register/',user_views.RegisterView.as_view(),name="register"),
   path('login/',user_views.LoginView.as_view(), name="login"),
   path('courses/',course_views.CourseManager.as_view()),
   path('areas/',area_views.AreaManager.as_view()),
   path('organizations/',organization_views.OrganizationManager.as_view()),
   path('email/',user_views.SendVerificationEmail.as_view()),
   path('main/',UserTemplate.user_list,name="main")
]
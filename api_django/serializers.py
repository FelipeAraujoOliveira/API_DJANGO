from rest_framework import serializers
from .models import User, Course

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','id_course','email','ra']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name','duration']
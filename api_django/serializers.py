from rest_framework import serializers
from .models import User, Course, Area, Organization

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','id_course','email','ra']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name','duration']

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id','name']

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id','name']
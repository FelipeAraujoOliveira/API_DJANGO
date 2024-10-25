from rest_framework import serializers
from .models import User, Course, Area, Organization
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        #fields = ['name','id_course','email','ra']
        fields = "__all__" 
        

    def create(self, valitaded_data):
        user = User(
            email = valitaded_data['email'],
            name=valitaded_data['name']
        )
        user.password = make_password(valitaded_data['password'])
        user.save()
        return user

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

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
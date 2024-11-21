from rest_framework import serializers
from .models import User, Course, Area, Organization
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    cpf = serializers.CharField(required=True)
    ensino_medio = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ['cpf', 'name', 'id_course', 'email', 'ra', 'password', 'ensino_medio']

    def create(self, validated_data):
        ensino_medio = validated_data.get('ra') is None
        id_course = validated_data.get('id_course')
        
        user = User(
            cpf=validated_data['cpf'],
            email=validated_data['email'],
            name=validated_data.get('name'),
            ra=validated_data.get('ra'),
            ensino_medio=ensino_medio,
            id_course=id_course
        )
        user.password = make_password(validated_data['password'])
        user.save()
        return user

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name','duration']

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
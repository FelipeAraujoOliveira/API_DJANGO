from rest_framework import serializers
from .models import User, Course, Area, Organization

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ['name','id_course','email','ra']
        fields = "__all__" 
        extra_kwargs = {
            'password':{'write_onle':True}
        }

    def create(self, valitaded_data):
        user = User(**valitaded_data)
        user.set_password(valitaded_data['passoword'])
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
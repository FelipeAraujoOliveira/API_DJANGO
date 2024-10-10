from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User,Course
from .serializers import UserSerializer,CourseSerializer

@api_view(['get'])
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
    
        return Response(serializer.data)
    
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_courses(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses,many=True)
        
        return Response(serializer.data)
    
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','POST','PUT','DELETE'])
def user_manager(request):
    if request.method == 'GET':
        try:
            if request.GET['email']:
                user_email = request.GET['email']

                try:
                    user = User.objects.get(email=user_email)
                    serializer = UserSerializer(user)
                    return Response(serializer.data)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'POST':
        new_user = request.data
        serializer = UserSerializer(data=new_user)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        user = request.data['email']

        try:
            updated_user = User.objects.get(email=user)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(updated_user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        try:
            user_to_delete = User.objects.get(email=request.data['email'])
            user_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
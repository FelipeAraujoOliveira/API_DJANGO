from django.shortcuts import render
from django.contrib.auth import authenticate,login as auth_login

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User,Course,Area,Organization
from .serializers import UserSerializer,CourseSerializer,AreaSerializer,OrganizationSerializer


@api_view(['GET','POST','PUT','DELETE'])
def user_manager(request):
    if request.method == 'GET':
        user_email = request.GET.get('email')
        if user_email:
            try:
                user = User.objects.get(email=user_email)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({'error':'User not found.'},status=status.HTTP_404_NOT_FOUND)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        try:
            updated_user = User.objects.get(email=request.data['email'])
            serializer = UserSerializer(updated_user, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        try:
            user_to_delete = User.objects.get(email=request.data['email'])
            user_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def course_manager(request):
    if request.method == 'GET':
        try:
            course_id = request.GET.get('id',None)
            if course_id:
                course = Course.objects.get(id=course_id)
                serializer = CourseSerializer(course)
                return Response(serializer.data)
            else:
                courses = Course.objects.all()
                serializer = CourseSerializer(courses,many=True)
                return Response(serializer.data)
        except Course.DoesNotExist:
            return Response({'error':'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        try:
            updated_course = Course.objects.get(id=request.data['id'])
            serializer = CourseSerializer(updated_course, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            course = Course.objects.get(id=request.data['id'])
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','POST','PUT','DELETE'])
def area_manager(request):
    if request.method == 'GET':
        try:
            area_id = request.GET.get('id',None)
            if area_id:
                area = Area.objects.get(id=area_id)
                serializer = AreaSerializer(area)
                return Response(serializer.data)
            else:
                areas = Area.objects.all()
                serializer = AreaSerializer(areas,many=True)
                return Response(serializer.data)
        except Area.DoesNotExist:
            return Response({'error':'Area not found.'},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = AreaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        try:
            updated_area = Area.objects.get(id=request.data['id'])
            serializer = AreaSerializer(updated_area, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            return Response(serializer.erros,status=status.HTTP_400_BAD_REQUEST)
        except Area.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'DELETE':
        try:
            area = Area.objects.get(id=request.data['id'])
            area.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Area.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def organization_manager(request):
    if request.method == 'GET':
        try:
            organization_id = request.GET.get('id', None)
            if organization_id:
                organization = Organization.objects.get(id=organization_id)
                serializer = OrganizationSerializer(organization)
                return Response(serializer.data)
            else:
                organizations = Organization.objects.all()
                serializer = OrganizationSerializer(organizations, many=True)
                return Response(serializer.data)
        except Organization.DoesNotExist:
            return Response({'error': 'Organization not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = OrganizationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        try:
            updated_organization = Organization.objects.get(id=request.data['id'])
            serializer = OrganizationSerializer(updated_organization, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Organization.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            organization = Organization.objects.get(id=request.data['id'])
            organization.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Organization.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    if email is None or password is None:
        return Response({'error':'Email e senha são obrigatórios.'},status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, email=email,password=password)

    if user is not None:
        return Response({'message':'Login bem-sucedido!','user':UserSerializer(user).data},status=status.HTTP_201_CREATED)
    
    return Response({'error':'Credenciais inválidas.'},status=status.HTTP_401_UNAUTHORIZED)
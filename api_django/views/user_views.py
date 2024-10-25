from django.contrib.auth import authenticate,get_user_model,login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import User
from ..serializers import UserSerializer,EmailVerificationSerializer
from dotenv import load_dotenv

import random, os

load_dotenv()

@api_view(['GET','PUT','DELETE'])
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
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if check_password(password, user.password):
        return Response({'message':'Login bem-sucedido!','user':UserSerializer(user).data},status=status.HTTP_202_ACCEPTED)    
    
    return Response({'error':'Credenciais inválidas.'},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def send_verification_email(request):
    serializer = EmailVerificationSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        code = random.randint(100000, 999999)

        subject = 'Código de verificação'
        message = f'Seu código de verificação é: {code}'
        from_email = os.getenv('EMAIL_HOST_USER')
        #from_email = settings.EMAIL_HOST_USER

        if not from_email:
            return Response({'error': 'E-mail do remetente não configurado.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            send_mail(
                subject,
                message,
                from_email,
                [email,'ianjabriel@hotmail.com'],
                fail_silently=False,
            )
            return Response({'message': 'E-mail enviado com sucesso!', 'code': code}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Ocorreu um erro ao enviar o e-mail: {e}")
            return Response({'error': 'Falha ao enviar o e-mail.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
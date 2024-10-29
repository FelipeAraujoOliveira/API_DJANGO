from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.core.cache import cache
from ..models import User
from ..serializers import UserSerializer, EmailVerificationSerializer
from dotenv import load_dotenv
import random, os

load_dotenv()

class UserManager(APIView):
    def get(self, request):
        user_email = request.GET.get('email')
        ensino_medio = request.GET.get('ensino_medio')
        
        if user_email:
            try:
                user = User.objects.get(email=user_email)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            users = User.objects.all()

            if ensino_medio is not None:
                if ensino_medio.lower() in ['true', '1']:
                    users = users.filter(ensino_medio=True)
                elif ensino_medio.lower() in ['false', '0']:
                    users = users.filter(ensino_medio=False)
                else:
                    return Response({'error': 'Valor inválido para ensino_medio. Use "true" ou "false".'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        try:
            updated_user = User.objects.get(email=request.GET.get('email'))
            serializer = UserSerializer(updated_user, data=request.data,partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        try:
            user_to_delete = User.objects.get(email=request.GET.get('email'))
            user_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        if email is None or password is None:
            return Response({'error': 'Email e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if check_password(password, user.password):
            return Response({'message': 'Login bem-sucedido!', 'user': UserSerializer(user).data}, status=status.HTTP_202_ACCEPTED)    
        
        return Response({'error': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)

class SendVerificationEmail(APIView):
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = random.randint(100000, 999999)
            cache.set(f'Códigode verificação de {email}: ', code, timeout=6000)

            subject = 'Código de verificação'
            message = f'Seu código de verificação é: {code}'
            from_email = os.getenv('EMAIL_HOST_USER')

            if not from_email:
                return Response({'error': 'E-mail do remetente não configurado.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    [email],
                    fail_silently=False,
                )
                return Response({'message': 'E-mail enviado com sucesso!', 'code': code}, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"Ocorreu um erro ao enviar o e-mail: {e}")
                return Response({'error': 'Falha ao enviar o e-mail.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
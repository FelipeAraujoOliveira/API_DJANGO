from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Organization
from ..serializers import OrganizationSerializer


class OrganizationManager(APIView):
    def get(self,request):
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
            return Response({'error': 'Organização não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self,request):
        serializer = OrganizationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        if not request.data.get('id'):
            return Response({'error':'Organização não encontrada.'},status=status.HTTP_404_NOT_FOUND)
        
        try:
            updated_organization = Organization.objects.get(id=request.data['id'])
            serializer = OrganizationSerializer(updated_organization, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Organization.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,request):
        try:
            organization = Organization.objects.get(id=request.data['id'])
            organization.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Organization.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
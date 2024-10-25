from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import User,Course,Area,Organization
from ..serializers import OrganizationSerializer

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
        
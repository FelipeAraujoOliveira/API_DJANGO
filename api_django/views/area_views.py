from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import Area
from ..serializers import AreaSerializer

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
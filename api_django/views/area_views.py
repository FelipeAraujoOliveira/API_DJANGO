from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Area
from ..serializers import AreaSerializer

class AreaManager(APIView):
    def get(self,request):
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
            return Response({'error':'Área não encontrada.'},status=status.HTTP_404_NOT_FOUND)

    def post(self,request):
        serializer = AreaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def put(self,request):
        if not request.data.get('id'):
            return Response({'error':'ID da área é obrigatório.'},status=status.HTTP_400_BAD_REQUEST)

        try:
            updated_area = Area.objects.get(id=request.data['id'])
            serializer = AreaSerializer(updated_area, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            return Response(serializer.erros,status=status.HTTP_400_BAD_REQUEST)
        except Area.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self,request):
        try:
            area = Area.objects.get(id=request.data['id'])
            area.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Area.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
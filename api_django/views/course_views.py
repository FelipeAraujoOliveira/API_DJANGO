from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import Course
from ..serializers import CourseSerializer

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
from rest_framework import generics 
from courses.models import Subject 
from .serializers import SubjectSerializer

class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer 

# building custom Views 
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Course

# adding authenticatiion & permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# class CourseEnrollView(APIView):
#     authentication_classes = (BasicAuthentication, )
#     permission_classes = (IsAuthenticated, )
#     def post(self, request, pk, format=None):
#        course = get_object_or_404(Course, pk=pk)
#        course.students.add(request.user)
#        return Response({
#            'enrolled': True
#        })

# creating a viewset 
from rest_framework import viewsets 
from .serializers import CourseSerializer
# additional actions to viewsets
from rest_framework.decorators import detail_route

# creating a view that mimics retrieve()
# but includes the course contents
from courses.api.permissions import IsEnrolled
from courses.api.serializers import CourseWithContentSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @detail_route(
        methods=['post'],
        authentication_classes=[BasicAuthentication], 
        permission_classes = [IsAuthenticated]                
    )

    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({
            'enrolled': True
        })
    
    @detail_route(
        ['get'], 
        serializer_class = CourseWithContentSerializer, 
        authentication_classes = [BasicAuthentication], 
        permission_classes = [IsAuthenticated, IsEnrolled]
    )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)




from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import InstituteSerializer,BatchSerializer
from .models import Institute,Batch
# Create your views here.


class InstituteCreate(APIView):
    permission_classes = [AllowAny]
    def post(self,request,*args,**kwargs):
        print(request.data,"just testing for bug????????")

        serializer =  InstituteSerializer(data = request.data)
        print(serializer)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
    def get(self, request, *args, **kwargs):
        
        institutes = Institute.objects.all()
        serializer = InstituteSerializer(institutes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    
class InstituteBatch(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = BatchSerializer(data=request.data)
        if serializer.is_valid():
            
            batch = serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request, *args, **kwargs):
        institute_id = kwargs.get('institute_id')  
        institute = get_object_or_404(Institute, id=institute_id)  

        batches = Batch.objects.filter(institute=institute)

        serializer = BatchSerializer(batches, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
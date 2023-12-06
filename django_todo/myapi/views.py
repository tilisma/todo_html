from django.shortcuts import render
from todoapp.models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny


# Create your views here.
class HomeView(APIView):
    permission_classes=[permissions.IsAuthenticated] 
    def get(self,request):
        userprofile = UserProfile.objects.get(user=request.user)
        ctask =Task.objects.filter(completed = True, created_by = userprofile)
        intask =Task.objects.filter(completed = False, created_by = userprofile)
        CSerializer = TaskSerializer(ctask,many=True).data
        inSerializer = TaskSerializer(intask,many=True).data
        data={
            'completed_task' : CSerializer,
            'incompleted_task' : inSerializer,
        }
        return Response(data,status=status.HTTP_200_OK)
    
    def post(self,request):
        userprofile = UserProfile.objects.get(user=request.user)
        alldata =request.data 
        alldata['created_by']= userprofile.id
        Serializer = TaskSerializer(data=alldata)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data,status=status.HTTP_200_OK)
        return Response(Serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UpdateTask(APIView):
    permission_classes=[permissions.IsAuthenticated] 
    def get(self,request,pk):
        task=Task.objects.get(id=pk)
        Serializer =TaskSerializer(task)
        return Response(Serializer.data,status=status.HTTP_200_OK)
    def patch(self,request,pk):
        task=Task.objects.get(id=pk)
        Serializer =TaskSerializer(task,data=request.data,partial=True) 
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data,status=status.HTTP_200_OK)
        return Response(Serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        task=Task.objects.get(id=pk)
        task.delete()
        return Response({"message:" "Task deleted Successfully"},status=status.HTTP_202_ACCEPTED)

class LoginView(TokenObtainPairView):
    permission_classes= (AllowAny,)
    serializer_class= UserTokenSerializer     


 
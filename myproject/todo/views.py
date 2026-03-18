from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Todo
from .serializers import Todoserializer

# Create your views here.

def home(request):
    return render(request, 'todo/home.html')


class TodoListApi(APIView):
    def post(self,request):
        serializer=Todoserializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        data=Todo.objects.all()
        serializer=Todoserializer(data,many=True)
        return Response(serializer.data)


class TodoListApi1(APIView):
    def get_object(self,pk):
        return get_object_or_404(Todo,pk=pk)
    def get(self,request,pk):
        # todo=Todo.objects.get(id=pk)
        todo=self.get_object(pk)

        if not todo:
            return Response({"error":"Not Found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer=Todoserializer(todo)
        return Response(serializer.data)
    
    def delete(self,request,pk):
        todo=self.get_object(pk)
        if not todo:
            return Response({"error":"Not Found"},status=status.HTTP_404_NOT_FOUND)
        todo.delete()
        return Response(status=204)
    
    def put(self,request,pk):
        todo=self.get_object(pk)
        if not todo:
            return Response({"error":"Not Found"},status=status.HTTP_404_NOT_FOUND)
        serializer=Todoserializer(todo,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)



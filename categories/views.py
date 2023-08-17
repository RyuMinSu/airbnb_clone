from django.shortcuts import render
from .models import Category

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .serializer import CategorySerializer

# from django.core import serializers
# from django.http import JsonResponse


# def categories(request):
#     all_categories = Category.objects.all()
#     return JsonResponse(
#         {
#             "ok":True,
#             "categories": serializers.serialize("json", all_categories)
#         }
#     )


class Categories(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            print(new_category)
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)
        
class CategoryDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise HTTP_204_NO_CONTENT
        

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)
    
    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
        


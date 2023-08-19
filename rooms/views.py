from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from .models import Amenity, Room
from .serializer import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from categories.models import Category



class Rooms(APIView):
    def get(self, request):
      all_rooms = Room.objects.all()
      serializer = RoomListSerializer(all_rooms, many=True)
      return Response(serializer.data)
    
    def post(self, request):        
        if request.user.is_authenticated: #유저인증
          serializer = RoomDetailSerializer(data=request.data)
          if serializer.is_valid():              
              # print("request_data:", request.data)
              category_pk = request.data.get("category")
              if not category_pk: #무조건 카테고리 입력 할 수 있도록
                  raise ParseError              
              try: #없는 카테고리를 입력할 경우
                  category = Category.objects.get(pk=category_pk)
                  if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                      raise ParseError
              except Category.DoesNotExist:
                  raise ParseError
              room = serializer.save(owner=request.user, category=category) # create의 validate에 자동 추가, 카테고리 추가
              serializer = RoomDetailSerializer(room)
              return Response(serializer.data)
          else:
              return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)

class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
          amenity = serializer.save()
          return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)

class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)        
    
    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
        
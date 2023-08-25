from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError,PermissionDenied
from .models import Amenity, Room
from .serializer import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from categories.models import Category
from reviews.serializer import ReviewSerializer



class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:  # 유저인증
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                # -----카테고리 추가
                category_pk = request.data.get("category")
                if not category_pk:  # 무조건 카테고리 입력 할 수 있도록
                    raise ParseError("Category is required")
                try:  # 없는 카테고리를 입력할 경우
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("카테고리가 존재하지 않음")
                except Category.DoesNotExist:
                    raise ParseError("카테고리 찾을 수 없음")
                
                try: # 트랜잭션 설정
                    with transaction.atomic():
                        room = serializer.save(
                            owner=request.user,
                            category=category,
                        )  # create의 validate에 자동 추가, 카테고리 추가

                        # ----- amenity추가(이건 create할때 필수로 입력 안해도됨)
                        amenities = request.data.get("amenities") # pk값 받아옴
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found")
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
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        room = self.get_object(pk)

        #----- 인증
        if not request.user.is_authenticated:
            return NotAuthenticated
        if room.owner != request.user:
            return PermissionDenied
        
        #----- back
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():        
            #----- category
            category_pk = request.data.get("category")
            if category_pk:
              try:
                  category = Category.objects.get(pk=category_pk)
                  if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                      raise ParseError("experience카테고리임")                
              except Category.DoesNotExist:
                  raise ParseError("없는 카테고리")
            
            try:
              with transaction.atomic():
                  #------ 값 업데이트
                  if category_pk == None:
                      room = serializer.save(owner=request.user)
                  else:                  
                      room = serializer.save(owner=request.user, category=category) 
                  
                  #----- amenity
                  amenities_pk = request.data.get("amenities") #list
                  if amenities_pk:
                      room.amenities.clear()
                      for amenity_pk in amenities_pk:                    
                          amenity = Amenity.objects.get(pk=amenity_pk)
                          room.amenities.add(amenity)
                  serializer = RoomDetailSerializer(room)
                  return Response(serializer.data)
            except Exception:
                return ParseError("없는 amenity")        
        else:
            return Response(serializer.errors)            

    
    def delete(self, request, pk):
        room = self.get_object(pk) # 해당 object찾기
        if not request.user.is_authenticated: #유저가 로그인 되어 있는지
            print("유저로그인 안되어있음")
            raise NotAuthenticated
        if room.owner != request.user: #유저와 해당 room의 owner가 일치하는지
            print("유저room과 owner안맞음")
            raise PermissionDenied
        room.delete()
        return Response(HTTP_204_NO_CONTENT)


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

class RoomReviews(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)            
        except ValueError:
            page = 1
        page_size = 3
        start = (page-1) * 3
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(room.reviews.all()[start:end], many=True)
        return Response(serializer.data)

        

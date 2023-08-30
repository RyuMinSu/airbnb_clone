from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from categories.models import Category
from .serializer import PerkSerializer, ExperienceSerializer, ExperienceDetailSerializer
from .models import Perk, Experience


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperienceList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(
            experiences,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)
    
    def post(self, request):        
        serializer = ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            #----- category
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("category 필수입력")
            try:
               category = Category.objects.get(pk=category_pk)
               if category.kind == Category.CategoryKindChoices.ROOMS:
                   raise ParseError("Experience만 가능")
            except Category.DoesNotExist:
                raise ParseError("없는 카테고리")
            
            try:
               with transaction.atomic():
                  experience = serializer.save(host=request.user, category=category)
                  #----- explanations
                  explanations_pk = request.data.get("explations")
                  if explanations_pk:
                     for explanation_pk in explanations_pk:
                        explanation = Perk.objects.get(pk=explanation_pk)
                        experience.explanations.add(explanation)
                  serializer = ExperienceDetailSerializer(experience, context={"request":request})
                  return Response(serializer.data)
            except Perk.DoesNotExist:
               raise ParseError("없는 Perk")
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):
   permission_classes = [IsAuthenticatedOrReadOnly]

   def get_experience(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound
   
   def get(self, request, pk):
        experience = self.get_experience(pk)
        serializer = ExperienceDetailSerializer(experience, context={"request":request})
        return Response(serializer.data)

   def delete(self, request, pk):            
      experience = self.get_experience(pk)
      if experience.host != request.user:
          raise PermissionDenied
      experience.delete()
      return Response(status=HTTP_204_NO_CONTENT)
   
   def put(self, request, pk):
      experience = self.get_experience(pk)      
      if experience.host != request.user:
          raise PermissionDenied
      
      serializer = ExperienceDetailSerializer(experience, data=request.data, partial=True)
      if serializer.is_valid():
         #----- category
         category_pk = request.data.get("category")
         if category_pk:
            try:
               category = Category.objects.get(pk=category_pk)
               if category.kind == Category.CategoryKindChoices.ROOMS:
                  raise ParseError("Experience만 됨")
            except Category.DoesNotExist:
               raise ParseError("카테고리없음")
         try:
            with transaction.atomic():
               if category_pk == None:
                  new_experience = serializer.save(host=request.user)
               else:
                  new_experience = serializer.save(host=request.user, category=category)
               #----- explanation
               explanation_pks = request.data.get("explanations")
               if explanation_pks:
                  new_experience.explanations.clear()
                  for explanation_pk in explanation_pks:                        
                     explanation = Perk.objects.get(pk=explanation_pk)
                     new_experience.explanations.add(explanation)
               serializer = ExperienceDetailSerializer(new_experience, context={"request":request})
               return Response(serializer.data)
         except Perk.DoesNotExist:
            raise ParseError("없는 explanation")
      else:
         return Response(serializer.errors)

          

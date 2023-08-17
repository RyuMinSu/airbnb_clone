from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Review


class RatingFilter(admin.SimpleListFilter):
   title = "Filter Rating"
   parameter_name = "potato"

   def lookups(self, request, model_admin):
      return [
         ("good", "Good"),
         ("bad", "Bad"),
      ]
   
   def queryset(self, request, reviews):
      rating_set = self.value()
      print(rating_set)
      if rating_set == "good":
         return reviews.filter(rating__gte=3)
      elif rating_set == "bad":
         return reviews.filter(rating__lt=3)
      else:
         return reviews


class WordFilter(admin.SimpleListFilter):
    title = "Filter words"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("nice", "Nice"),
        ]
    
    def queryset(self, request, reviews): # reviews: 필터링 됐을때 리뷰들
        print(request.GET)
        print(self.value())
        word = self.value()
        if word:
          return reviews.filter(payload__contains=word)
        else:
          return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        "user__is_host",
        "room__category",
        "room__pet_friendly",
        WordFilter,
        RatingFilter,
    )

from django.db import models
from common.models import CommonModel


# Create your models here.
class Experience(CommonModel):
    
    """ Experience Model Definition """

    country = models.CharField(max_length=50, default="한국",)
    city = models.CharField(max_length=80, default="서울",)
    name = models.CharField(max_length=250,)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="experiences",)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end= models.TimeField()
    description = models.TextField(default="", blank=True,)
    explanations = models.ManyToManyField("experiences.Perk", related_name="experiences",)
    category = models.ForeignKey("categories.Category", on_delete=models.SET_NULL, null=True, blank=True, related_name="experiences",)


    def average_ratings(experience):
        reviews_count = experience.reviews.count()
        if reviews_count == 0:
            return 0
        else:
            ratings = experience.reviews.all().values("rating")
            total_rating = 0
            for rating in ratings:
                total_rating += rating["rating"]
            return (total_rating / reviews_count)
        

    def __str__(self) -> str:
        return self.name
    
    


class Perk(CommonModel):
    """ What is included on an Experiences"""
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=250, blank=True, default="",)
    explanation = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return self.name


    
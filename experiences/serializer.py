from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.serializer import TinyUserSerializer
from wishlists.models import Wishlist
from categories.serializer import CategorySerializer
from .models import Perk, Experience


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = ("pk", "name", "details", "explanation")



class ExperienceSerializer(ModelSerializer):
    
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = ("id", "name", "country", "city", "price", "is_owner", "rating", "is_liked")
    
    def get_is_owner(self, experience):
        request = self.context["request"]        
        return experience.host == request.user
    
    def get_is_liked(self, experience):
        request = self.context["request"]
        wish = Wishlist.objects.filter(user=request.user, experiences__pk=experience.pk)
        return wish.exists()
    
    def get_rating(self, experience):
        return experience.average_ratings()
        

class ExperienceDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    explanations = PerkSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    

    class Meta:
        model = Experience
        fields = "__all__"

    def get_is_owner(self, experience):
        request = self.context["request"]
        return experience.host == request.user        

    def get_is_liked(self, experience):
        request = self.context["request"]
        wish = Wishlist.objects.filter(user=request.user, experiences__pk=experience.pk)
        return wish.exists()

    def get_rating(self, experience):
        return experience.average_ratings()


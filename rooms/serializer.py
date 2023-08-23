from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from users.serializer import TinyUserSerializer
from categories.serializer import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description",)


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = SerializerMethodField()

    class Meta:        
        model = Room
        fields = "__all__"

    def get_rating(self, room):        
        return room.rating()
        


    # def create(self, validated_data):
    #     print(validated_data)
    #     return 

        
class RoomListSerializer(ModelSerializer):
    rating = SerializerMethodField()
    class Meta:
        model = Room
        fields = ("id", "country", "city", "price", "rating")

    def get_rating(self, room):
        return room.rating()


from rest_framework.serializers import ModelSerializer
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

    class Meta:        
        model = Room
        fields = "__all__"

class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "country", "city", "price",)


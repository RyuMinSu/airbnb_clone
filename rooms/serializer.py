from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from users.serializer import TinyUserSerializer
from categories.serializer import CategorySerializer
from reviews.serializer import ReviewSerializer
from medias.serializer import PhotoSerializer
from wishlists.models import Wishlist




class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("pk", "name", "description",)


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = SerializerMethodField()
    is_ownser = SerializerMethodField()
    is_liked = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)


    class Meta:        
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_ownser(self, room): # view에서 보낸 데이터로 새로운 method만들 수 있음
        request = self.context['request']
        if request:
            return room.owner == request.user
        return False
    
    def get_is_liked(self, room):
        request = self.context['request']
        #user의 wishlists들을 찾는다 > 찾은 wishlist에서 해당 room을 찾는다
        if request:
            if request.user.is_authenticated:
                return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists()
        return False




    # def create(self, validated_data):
    #     print(validated_data)
    #     return 

        
class RoomListSerializer(ModelSerializer):
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ("id", "country", "city", "price", "rating", "is_owner", "photos")

    def get_rating(self, room):
        return room.rating()
    
    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user


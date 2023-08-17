from django.contrib import admin
from .models import Room, Amenity

@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    
    #액션 함수 추가
    actions = (reset_prices,)

    list_display = ("name", "price", "kind", "total_amenities", "rating", "owner", "created_at",)
    list_filter = ("country", "city", "pet_friendly", "kind", "amenities", "created_at", "updated_at")
    search_fields = ("owner__username",) # startswith: ^, 100%equal: =price, ForeignKey로 찾을때: 외래키로 적용되어있는 필드 + __참조하는모델의 필드

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at",)
    readonly_fields = ("created_at", "updated_at",)
        
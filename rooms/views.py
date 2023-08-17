from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


# Create your views here.
def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "all_rooms.html",
        context={
            "rooms": rooms,
            "title": "render title",
        },
    )


def see_one_rooms(request, room_pk):
    try:
      room = Room.objects.get(pk=room_pk)
      return render(request, "room_detail.html", context={"room": room})
    except Room.DoesNotExist:
      return render(request, "room_detail.html", context={"not_found":True})

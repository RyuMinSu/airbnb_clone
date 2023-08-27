from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Booking


class CreateBookingSerializer(ModelSerializer):
    # model에서는 필수가 아니지만 이 클래스에서는 필수로 덮어쓰기
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    # validate customizing
    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't booking past")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't booking past")
        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out"
            )
        if Booking.objects.filter(check_in__lte=data["check_out"], check_out__gte=data["check_in"],).exists():
            raise serializers.ValidationError("already booking")
        return data


class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )

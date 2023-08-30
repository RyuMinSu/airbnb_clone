from django.urls import path
from .views import Perks, PerkDetail, ExperienceList, ExperienceDetail



urlpatterns = [
	path("", ExperienceList.as_view()),
	path("<int:pk>", ExperienceDetail.as_view()),
	path("perks/", Perks.as_view()),
	path("perks/<int:pk>", PerkDetail.as_view()),
]
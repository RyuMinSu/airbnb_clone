from django.test import TestCase
from rest_framework.test import APITestCase
from . import models


class TestAmenities(APITestCase):
	NAME = "Amenity Test"
	DESC = "Amenity Description"

	def setUp(self):
		models.Amenity.objects.create(name=self.NAME, description=self.DESC,)
	
	def test_all_amenities(self):
		response = self.client.get("/api/v1/rooms/amenities")
		data = response.json()
		print(data)
		# get으로 접속 되는지
		self.assertEqual(response.status_code, 200, msg="wrong")
		# 반환되는 data가 list가 맞는지
		self.assertIsInstance(data, list)
		# 반환된 data에 1개만 들었는지
		self.assertEqual(len(data), 1)
		# data.name == self.NAME
		self.assertEqual(data[0]["name"], self.NAME)
		# data.description == self.DESC
		self.assertEqual(data[0]["description"], self.DESC)

from django.test import TestCase
from rest_framework.test import APITestCase
from . import models


class TestAmenities(APITestCase):
	NAME = "Amenity Test"
	DESC = "Amenity Description"
	URL = "/api/v1/rooms/amenities"

	def setUp(self):
		models.Amenity.objects.create(name=self.NAME, description=self.DESC,)
	
	def test_all_amenities(self):
		response = self.client.get(self.URL)
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

	def test_post_amenities(self):
		new_amenity = "new amenity"
		new_desc = "new description"

		#----- 데이터를 넣은상태
		response = self.client.post(self.URL, data={"name": new_amenity, "description": new_desc})
		data = response.json()
		# post가 잘 동작 하는지
		self.assertEqual(response.status_code, 200, "not 200")
		# 들어간 데이터와 보낸 데이터가 맞는지
		self.assertEqual(data["name"], new_amenity,)
		self.assertEqual(data["description"], new_desc,)

		#------ 데이터를 넣지 않은 상태 -> serializer.errors, badrequest
		response = self.client.post(self.URL)
		data = response.json()
		# post가 잘 동작 하는지(badrequest)
		self.assertEqual(response.status_code, 400,)
		# 에러문구 나오는지 (serializer.errors)
		self.assertIn("name", data)



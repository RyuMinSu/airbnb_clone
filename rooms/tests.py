from django.test import TestCase
from rest_framework.test import APITestCase
from . import models


#----- Amenity
class TestAmenities(APITestCase):
	NAME = "Amenity Test"
	DESC = "Amenity Description"
	URL = "/api/v1/rooms/amenities"

	def setUp(self):
		models.Amenity.objects.create(name=self.NAME, description=self.DESC,)
	
	def test_all_amenities(self):
		response = self.client.get(self.URL)
		data = response.json()		
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


#----- Amenity Detail
class TestAmenity(APITestCase):
	NAME = "Amenity Test"
	DESC = "Amenity Description"

	def setUp(self):
		models.Amenity.objects.create(name=self.NAME, description=self.DESC,)

	#----- get_object
	def test_amenity_not_found(self):
		# False
		response = self.client.get("/api/v1/rooms/amenities/2")
		self.assertEqual(response.status_code, 404, "have to 404")

	#------ get
	def test_get_amenity(self):		
		# get_object == True
		response = self.client.get("/api/v1/rooms/amenities/1")
		data = response.json()
		#----- get일 경우
		# 잘 작동하는지
		self.assertEqual(response.status_code, 200, "dpd")
		# 잘 받아오는지
		self.assertEqual(data["name"], self.NAME, "not name")
		self.assertEqual(data["description"], self.DESC, "not desc")

	#----- delete
	def test_delete_amenity(self):
		response = self.client.delete("/api/v1/rooms/amenities/1")
		self.assertEqual(response.status_code, 204)

	#----- put
	def test_put_amenity(self):
		update_name = "new_amenity2"
		update_desc = "new_desc2"
		update_name_over150 = "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
		

		#----- 데이터 입력 됐을때
		# get_object == True
		response = self.client.put("/api/v1/rooms/amenities/1", data={"name": update_name, "description": update_desc},)
		data = response.json()
		# 잘 동작 하는지
		self.assertEqual(response.status_code, 200, "update error")
		#잘 변경됐는지
		self.assertEqual(data["name"], update_name, "update name wrong")
		self.assertEqual(data["description"], update_desc, "update desc wrong")

		#----- 데이터 입력 안됐을때
		response = self.client.put("/api/v1/rooms/amenities/1", data={"name": update_name_over150})
		# badrequest 나오는지
		self.assertEqual(response.status_code, 400, "not bad request")
		# serializer.errors 나오는지
		self.assertIn("name", response.json())





		

from rest_framework.views import APIView
from rest_framework.response import Response
import json

from backend.services import DatabaseinterfacesService

class DatabaseinterfacesView(APIView):

	def get(self, request):
		result = DatabaseinterfacesService.readAll()
		return Response(result)

	def post(self, request):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = DatabaseinterfacesService.createOne(**json_dict)
		return Response(result)

class DatabaseinterfacesDetailView(APIView):

	def get(self, request, id):
		result = DatabaseinterfacesService.readOne(id)
		return Response(result)

	def put(self, request, id):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = DatabaseinterfacesService.updateOne(id, json_dict)
		return Response(result)

	def delete(self, request, id):
		result = DatabaseinterfacesService.deleteOne(id)
		return Response(result)
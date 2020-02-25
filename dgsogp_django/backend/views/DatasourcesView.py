from rest_framework.views import APIView
from rest_framework.response import Response
import json

from backend.services import DatasourcesService

class DatasourcesView(APIView):

	def get(self, request):
		result = DatasourcesService.readAll()
		return Response(result)

	def post(self, request):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = DatasourcesService.createOne(**json_dict)
		return Response(result)

class DatasourcesDetailView(APIView):

	def get(self, request, id):
		result = DatasourcesService.readOne(id)
		return Response(result)

	def put(self, request, id):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = DatasourcesService.updateOne(id, json_dict)
		return Response(result)

	def delete(self, request, id):
		result = DatasourcesService.deleteOne(id)
		return Response(result)
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from backend.services import HadoopsourcesService

class HadoopsourcesView(APIView):

	def get(self, request):
		result = HadoopsourcesService.readAll()
		return Response(result)

	def post(self, request):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = HadoopsourcesService.createOne(**json_dict)
		return Response(result)

class HadoopsourcesDetailView(APIView):

	def get(self, request, id):
		result = HadoopsourcesService.readOne(id)
		return Response(result)

	def put(self, request, id):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = HadoopsourcesService.updateOne(id, json_dict)
		return Response(result)

	def delete(self, request, id):
		result = HadoopsourcesService.deleteOne(id)
		return Response(result)
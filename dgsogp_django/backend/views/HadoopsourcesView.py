from rest_framework.views import APIView
from rest_framework.response import Response
import json

from backend.services import HadoopsourcesService

class HadoopsourcesView(APIView):

	def get(self, request):
		pageIndex = request.GET.get('pageIndex')
		pageSize = request.GET.get('pageSize')
		select = request.GET.get('select')
		key = request.GET.get('key')
		if select and key:
			result = HadoopsourcesService.readByCondition(pageIndex, pageSize, select, key)
			return Response(result)
		else:
			result = HadoopsourcesService.readPage(pageIndex, pageSize)
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
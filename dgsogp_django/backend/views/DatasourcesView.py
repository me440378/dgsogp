from rest_framework.views import APIView
from rest_framework.response import Response
import json

from backend.services import DatasourcesService

class DatasourcesView(APIView):

	def get(self, request):
		pageIndex = request.GET.get('pageIndex')
		pageSize = request.GET.get('pageSize')
		select = request.GET.get('select')
		key = request.GET.get('key')
		if select and key:
			result = DatasourcesService.readByCondition(pageIndex, pageSize, select, key)
			return Response(result)
		else:
			result = DatasourcesService.readAll(pageIndex, pageSize)
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
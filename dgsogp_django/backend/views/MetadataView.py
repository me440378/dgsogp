from rest_framework.views import APIView
from rest_framework.response import Response
import json

from backend.services import MetadataService

class MetadataView(APIView):

	def get(self, request):
		pageIndex = request.GET.get('pageIndex')
		pageSize = request.GET.get('pageSize')
		select = request.GET.get('select')
		key = request.GET.get('key')
		if select and key:
			result = MetadataService.readByCondition(pageIndex, pageSize, select, key)
			return Response(result)
		else:
			result = MetadataService.readAll(pageIndex, pageSize)
			return Response(result)

	def post(self, request):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = MetadataService.createOne(**json_dict)
		return Response(result)

class MetadataDetailView(APIView):

	def get(self, request, id):
		result = MetadataService.readOne(id)
		return Response(result)

	def put(self, request, id):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = MetadataService.updateOne(id, json_dict)
		return Response(result)

	def delete(self, request, id):
		result = MetadataService.deleteOne(id)
		return Response(result)
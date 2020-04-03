from rest_framework.views import APIView
from rest_framework.response import Response
import json

from backend.services import DatainterfacesService

class DatainterfacesView(APIView):

	def get(self, request):
		pageIndex = request.GET.get('pageIndex')
		pageSize = request.GET.get('pageSize')
		select = request.GET.get('select')
		key = request.GET.get('key')
		if select and key:
			result = DatainterfacesService.readPageByCondition(pageIndex, pageSize, select, key)
			return Response(result)
		else:
			result = DatainterfacesService.readPage(pageIndex, pageSize)
			return Response(result)

	def post(self, request):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = DatainterfacesService.createOne(**json_dict)
		return Response(result)

class DatainterfacesDetailView(APIView):

	def get(self, request, id):
		result = DatainterfacesService.readOne(id)
		return Response(result)

	def put(self, request, id):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = DatainterfacesService.updateOne(id, json_dict)
		return Response(result)

	def delete(self, request, id):
		result = DatainterfacesService.deleteOne(id)
		return Response(result)

class DatainterfacesDataView(APIView):
	
	def get(self, request, id):
		result = DatainterfacesService.readData(id)
		return Response(result)
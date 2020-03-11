from backend.models import Datainterfaces
from backend.serializers import DatainterfacesSerializer
from backend.tools import reply
from backend.tools import countReply

class DatainterfacesService():
	
	def createOne(type, name, metadata_id):
		try:
			datainterface = Datainterfaces.objects.using('admin_db').create(
				type = type,
				name = name,
				metadata_id = metadata_id,
			)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def readAll():
		re = None
		try:
			re = Datainterfaces.objects.using('admin_db').all()
			result = DatainterfacesSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def readOne(id):
		re = None
		try:
			re = Datainterfaces.objects.using('admin_db').get(pk = id)
			result = DatainterfacesSerializer(re)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def updateOne(id, kvdict):
		try:
			Datainterfaces.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def deleteOne(id):
		try:
			Datainterfaces.objects.using('admin_db').filter(pk = id).delete()
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def countAll():
		re = None
		try:
			re = Datainterfaces.objects.using('admin_db').count()
		except Exception as e:
			return reply(1, str(e))
		return re
		
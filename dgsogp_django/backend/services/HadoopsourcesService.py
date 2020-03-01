from backend.models import Hadoopsources
from backend.serializers import HadoopsourcesSerializer
from backend.tools import reply

class HadoopsourcesService():

	def createOne(state, source, datasource_id):
		try:
			Hadoopsources = Hadoopsources.objects.using('admin_db').create(
				state = state,
				source = source,
				datasource_id = datasource_id,
			)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def readAll():
		re = None
		try:
			re = Hadoopsources.objects.using('admin_db').all()
			result = HadoopsourcesSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def readOne(id):
		re = None
		try:
			re = Hadoopsources.objects.using('admin_db').get(pk = id)
			result = HadoopsourcesSerializer(re)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def updateOne(id, kvdict):
		try:
			Hadoopsources.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def deleteOne(id):
		try:
			Hadoopsources.objects.using('admin_db').filter(pk = id).delete()
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

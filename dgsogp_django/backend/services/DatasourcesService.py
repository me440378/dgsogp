from backend.models import Datasources
from backend.serializers import DatasourcesSerializer
from backend.tools import reply

class DatasourcesService():
	
	def createOne(wgroup, wserver, type, source, related, state, excepted, putindb = None, pattern = None, target = None, content = None):
		try:
			datasource = Datasources.objects.using('admin_db').create(
				wgroup = wgroup,
				wserver = wserver,
				type = type,
				source = source,
				putindb = putindb,
				related = related,
				pattern = pattern,
				target = target,
				state = state,
				content = content,
				excepted = excepted,
			)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def readAll():
		re = None
		try:
			re = Datasources.objects.using('admin_db').all()
			result = DatasourcesSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def readOne(id):
		re = None
		try:
			re = Datasources.objects.using('admin_db').get(pk = id)
			result = DatasourcesSerializer(re)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def updateOne(id, kvdict):
		try:
			Datasources.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def deleteOne(id):
		try:
			Datasources.objects.using('admin_db').filter(pk = id).delete()
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def finishOne(id):
		kvdict = {"state":2}
		try:
			Datasources.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)
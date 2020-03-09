# from backend.models import Datasources
# from backend.serializers import DatasourcesSerializer
from backend.models import Datasources
from backend.models import Hadoopsources
from backend.models import Metadata
from backend.services import UsersService
from backend.services import DatasourcesService
from backend.services import HadoopsourcesService
from backend.services import MetadataService
from backend.tools import reply

class FrontendService():

	def getDashboardData(userid):
		user = UsersService.readOne(userid)
		datasourcesCount = DatasourcesService.countAll()
		hadoopsourcesCount = HadoopsourcesService.countAll()
		metadataCount = MetadataService.countAll()
		usersCount = UsersService.countAll()
		return {
			"user": user,
			"datasourcesCount": datasourcesCount,
			"hadoopsourcesCount": hadoopsourcesCount,
			"metadataCount": metadataCount,
			"usersCount" : usersCount,
		}

	def getHeaderData(userid):
		user = UsersService.readOne(userid)
		return {
			"user": user
		}

	def finishDatasourceState(datasource_id):
		try:
			if Hadoopsources.objects.using('admin_db').filter(datasource_id = datasource_id):
				DatasourcesService.finishOne(datasource_id)
				hadoopsource = Hadoopsources.objects.using('admin_db').filter(datasource_id = datasource_id)[0]
				hadoopsource_id = hadoopsource.id
				HadoopsourcesService.prefinishOne(hadoopsources_id)
				metadataList = Metadata.objects.using('admin_db').filter(hadoopsource_id = hadoopsource_id)
				for metadata in metadataList:
					metadata_id = metadata.id
					MetadataService.prefinishOne(metadataid)
			else:
				#还没有对应的Hadoopsources
				DatasourcesService.prefinishOne(datasource_id)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)
		
	
	# def createOne(wgroup, wserver, type, source, related, state, excepted, putindb = None, pattern = None, target = None, content = None):
	# 	try:
	# 		datasource = Datasources.objects.using('admin_db').create(
	# 			wgroup = wgroup,
	# 			wserver = wserver,
	# 			type = type,
	# 			source = source,
	# 			putindb = putindb,
	# 			related = related,
	# 			pattern = pattern,
	# 			target = target,
	# 			state = state,
	# 			content = content,
	# 			excepted = excepted,
	# 		)
	# 	except Exception as e:
	# 		return reply(1, str(e))
	# 	return reply(0)

	# def readAll():
	# 	re = None
	# 	try:
	# 		re = Datasources.objects.using('admin_db').all()
	# 		result = DatasourcesSerializer(re, many = True)
	# 	except Exception as e:
	# 		return reply(1, str(e))
	# 	return result.data

	# def readOne(id):
	# 	re = None
	# 	try:
	# 		re = Datasources.objects.using('admin_db').get(pk = id)
	# 		result = DatasourcesSerializer(re)
	# 	except Exception as e:
	# 		return reply(1, str(e))
	# 	return result.data

	# def updateOne(id, kvdict):
	# 	try:
	# 		Datasources.objects.using('admin_db').filter(pk = id).update(**kvdict)
	# 	except Exception as e:
	# 		return reply(1, str(e))
	# 	return reply(0)

	# def deleteOne(id):
	# 	try:
	# 		Datasources.objects.using('admin_db').filter(pk = id).delete()
	# 	except Exception as e:
	# 		return reply(1, str(e))
	# 	return reply(0)

	# def finishOne(id):
	# 	kvdict = {"state":2}
	# 	try:
	# 		Datasources.objects.using('admin_db').filter(pk = id).update(**kvdict)
	# 	except Exception as e:
	# 		return reply(1, str(e))
	# 	return reply(0)
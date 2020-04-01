from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from backend.models import Hadoopsources
from backend.serializers import HadoopsourcesSerializer
from backend.tools import reply, dtReply

class HadoopsourcesService():

	def createOne(state, source, datasource_id):
		try:
			hadoopsources = Hadoopsources.objects.using('admin_db').create(
				state = state,
				source = source,
				datasource_id = datasource_id,
			)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def readAll():
		try:
			re = Hadoopsources.objects.using('admin_db').all()
			result = HadoopsourcesSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def readPage(pageIndex, pageSize):
		try:
			re = Hadoopsources.objects.using('admin_db').all()
			paginator = Paginator(re, pageSize)
			page = paginator.page(pageIndex)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_page)
		except Exception as e:
			return reply(1, str(e))
		result = HadoopsourcesSerializer(page, many = True)
		total = Hadoopsources.objects.using('admin_db').count()
		return dtReply(result.data, total)

	def readByCondition(pageIndex, pageSize, select, key):
		try:
			kvdict = {select: key}
			re = Hadoopsources.objects.using('admin_db').filter(**kvdict)
			paginator = Paginator(re, pageSize)
			page = paginator.page(pageIndex)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_page)
		except Exception as e:
			return reply(1, str(e))
		result = HadoopsourcesSerializer(page, many = True)
		total = re.count()
		return dtReply(result.data, total)

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

	def prefinishOne(id):
		kvdict = {"state":0}
		try:
			Hadoopsources.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def finishOne(id):
		kvdict = {"state":2}
		try:
			Hadoopsources.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)
		
	def countAll():
		re = None
		try:
			re = Hadoopsources.objects.using('admin_db').count()
		except Exception as e:
			return reply(1, str(e))
		return re
		
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from backend.models import Messages
from backend.serializers import MessagesSerializer
from backend.tools import reply, dtReply

class MessagesService():

	def createOne(name, content, status = 0):
		try:
			message = Messages.objects.using('admin_db').create(
				name = name,
				content = content,
				status = status,
			)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def readAll():
		try:
			re = Messages.objects.using('admin_db').all()
			result = MessagesSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def readPage(pageIndex, pageSize):
		try:
			re = Messages.objects.using('admin_db').all()
			paginator = Paginator(re, pageSize)
			page = paginator.page(pageIndex)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_page)
		except Exception as e:
			return reply(1, str(e))
		result = MessagesSerializer(page, many = True)
		total = Messages.objects.using('admin_db').count()
		return dtReply(result.data, total)

	def readPageByCondition(pageIndex, pageSize, select, key):
		try:
			kvdict = {select: key}
			re = Messages.objects.using('admin_db').filter(**kvdict)
			paginator = Paginator(re, pageSize)
			page = paginator.page(pageIndex)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_page)
		except Exception as e:
			return reply(1, str(e))
		result = MessagesSerializer(page, many = True)
		total = re.count()
		return dtReply(result.data, total)

	def readOne(id):
		re = None
		try:
			re = Messages.objects.using('admin_db').get(pk = id)
			result = MessagesSerializer(re)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def readByCondition(select, key):
		try:
			kvdict = {select: key}
			re = Messages.objects.using('admin_db').filter(**kvdict)
			result = MessagesSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def updateOne(id, kvdict):
		try:
			Messages.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def deleteOne(id):
		try:
			Messages.objects.using('admin_db').filter(pk = id).delete()
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def countAll():
		re = None
		try:
			re = Messages.objects.using('admin_db').count()
		except Exception as e:
			return reply(1, str(e))
		return re

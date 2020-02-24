from backend.models import Users
from backend.serializers import UsersSerializer
from backend.tools import reply
from backend.tools import md5hash

class UsersService():
	
	def register(username, password, nickname):
		re = None
		try:
			re = Users.objects.filter(username = username)
		except Exception as e:
			return reply(1, str(e))

		if re:
			return reply(1, '该用户名已存在')
		else:
			try:
				user = Users.objects.create(
					username = username,
					nickname = nickname,
					password = md5hash(password),
				)
			except Exception as e:
				return reply(1, str(e))
		return reply(0)

	def getAll():
		re = None
		try:
			re = Users.objects.all()
			result = UsersSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data
		
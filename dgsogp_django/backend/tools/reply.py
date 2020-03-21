#简单回复
def reply(error, detail = None):
	if error == 0:
		return {'error': error}
	else:
		return {'error': error, 'detail': detail}

#数量回复
def countReply(count):
	return {'count': count}

#数据与总条数回复
def dtReply(data, total):
	return {'data': data, 'total': total}
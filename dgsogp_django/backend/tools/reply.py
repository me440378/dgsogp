#简单回复
def reply(error, detail = None):
	if error == 0:
		return {'error': error}
	else:
		return {'error': error,'detail': detail}

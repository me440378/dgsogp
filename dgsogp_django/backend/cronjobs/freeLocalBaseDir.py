import os
#local
from backend.tools import deleteFileOrDir

def freeLocalBaseDir():
	localBase = r'./tmp'
	for wgroup in os.listdir(localBase):
		for wserver in os.listdir(''.join([localBase, '/', wgroup])):
			for f in os.listdir(''.join([localBase, '/', wgroup, '/', wserver])):
				fullf = ''.join([localBase, '/', wgroup, '/', wserver, '/', f])
				deleteFileOrDir(fullf)
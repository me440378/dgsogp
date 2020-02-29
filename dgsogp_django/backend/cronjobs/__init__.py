# from . import *

def testjob():
	import time
	print('crontab-test 2min print1,{}'.format(time.time()))

#从工作服务器采集到hadoop集群
def collectDataFromServers():
	pass

#扫描hadoop集群上的文件，入库
def scanHadoopPutInDB():
	pass

#扫描hadoop集群上的文件，标记
def scanHadoopTagMetadata():
	pass
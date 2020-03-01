from .scanDatasourcesToHadoop import *
from .scanHadoopPutInDB import *
from .scanHadoopTagMetadata import *

def testjob():
	import time
	print('crontab-test 2min print1,{}'.format(time.time()))

#从工作服务器采集到hadoop集群
def collectDataFromServers():
	pass
	# 判断状态是什么
	# 	已完成
	# 		不用管
	# 	未处理、处理中
	# 		判断是否为文件、目录
	# 			否
	# 				先不用管
	# 			是
	# 				从本地目录写入hdfs
	# 					未处理的将处理状态改为已完成


#从远端采集到本地再上传HDFS，创建Hadoopsources
from .collectDataFromServers import *
#将HDFS上的文件下载到本地，创建Metadata
from .scanHadoopTagMetadata import *
#将HDFS上的文件下载到本地，根据Metadata入库
from .scanMetadataPutInDB import *
#清空本地暂存目录
from .freeLocalBaseDir import *

def testjob():
	import time
	print('crontab-test 2min print1,{}'.format(time.time()))


from .collectDataFromServers import *
from .scanHadoopTagMetadata import *
from .scanMetadataPutInDB import *

def testjob():
	import time
	print('crontab-test 2min print1,{}'.format(time.time()))


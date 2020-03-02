from .collectDataFromServers import *
from .scanDatasourcesToHadoopsources import *
from .scanHadoopPutInDB import *
from .scanHadoopTagMetadata import *

def testjob():
	import time
	print('crontab-test 2min print1,{}'.format(time.time()))


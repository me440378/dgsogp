import paramiko
from hdfs import InsecureClient

from backend.services import DatasourcesService
from backend.tools import get_all_files_in_remote_dir
from backend.tools import makeLocalPath
from backend.tools import makeHdfsPath
from backend.tools import getDir

#从工作服务器采集到hadoop集群
def collectDataFromServers():
	localBase = r'./tmp'
	DatasourcesList = DatasourcesService.readAll()
	for Datasources in DatasourcesList:
		# 判断状态是什么
		state = Datasources['state']#0 未处理、1 处理中、2 已完成
		if (state == 0) or (state == 1):
			# 未处理、处理中
			wgroup = Datasources['wgroup']
			wserver = Datasources['wserver']
			localGaS = ''.join([localBase, '/', wgroup, '/', wserver])#./tmp/group/server
			hadoopGaS = ''.join(['/', wgroup, '/', wserver])#/group/server
			source = Datasources['source']
			target = Datasources['target']
			#获取sftp客户端
			SftpClint = getSftpClient(wserver)
			#获取Hadoop客户端
			HadoopClient = getHadoopClient()
			# 判断是否为文件、目录
			type = Datasources['type']#0 文件、1 目录、3 数据库
			if type == 0:
				# 文件
				# 将文件写入本地
				remote = source
				local = localGaS + target
				localDir = getDir(local)
				makeLocalPath(localDir)
				SftpClint.get(remote, local)#下载
				SftpClint.close()
				# 从本地上传到hadoop
				hpath = hadoopGaS + target#/dev/server/iris.data
				hpathDir = getDir(hpath)#/dev/server
				makeHdfsPath(HadoopClient, hpathDir)
				HadoopClient.upload(hpath, local)
			elif type == 1:
				# 目录
				localRootDir = localGaS + target#./tmp/ops/server/python
				remoteDir = source
				# 将目录所有文件递归列出列表
				remoteList = get_all_files_in_remote_dir(SftpClint, remoteDir)
				# 将列表中的全部文件写入本地
				for remote in remoteList:
					local = localRootDir + remote[len(remoteDir):]
					localDir = getDir(local)
					makeLocalPath(localDir)
					SftpClint.get(remote, local)#下载
					# 将本地文件上传到hadoop
					hpath = hadoopGaS + target + remote[len(remoteDir):]
					hpathDir = getDir(hpath)
					makeHdfsPath(HadoopClient, hpathDir)
					HadoopClient.upload(hpath, local)
				SftpClint.close()
			elif type == 2:
				# 数据库，先不用管
				pass
		elif state == 2:
			# 已完成，不用管
			pass

def getSftpClient(wserver):
	#密钥登录
	privage_key = paramiko.RSAKey.from_private_key_file('./ssh-key/hadoop_cluster')
	t=paramiko.Transport((wserver, 22))#ftp
	t.connect(username = 'root',pkey=privage_key)
	SftpClient = paramiko.SFTPClient.from_transport(t)
	return SftpClient

def getHadoopClient():
	return InsecureClient('http://hadoop-server-test:50070', user='hadoop', root='/')

def putOnHadoop():
	pass

def genHadoopSources():
	pass

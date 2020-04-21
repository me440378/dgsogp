from hdfs import InsecureClient

from dgsogp_django.settings import HADOOP_BASE

def getHadoopClient():
	return InsecureClient(**HADOOP_BASE)

def makeHdfsPath(client, hdfsPath):
    if not client.status(hdfsPath,strict=False):
        client.makedirs(hdfsPath)

def getAllFilesInHadoopDir(client, remote_dir):
    # 保存所有文件的列表
    all_files = list()
    # 去掉路径字符串最后的字符'/'，如果有的话
    if remote_dir[-1] == '/':
        remote_dir = remote_dir[0:-1]
    # 获取当前指定目录下的所有目录及文件，包含属性值
    files = client.list(remote_dir)
    for x in files:
        # remote_dir目录中每一个文件或目录的完整路径
        filename = remote_dir + '/' + x
        # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
        if client.status(filename)['type'] == 'DIRECTORY':
            all_files.extend(getAllFilesInHadoopDir(client, filename))
        else:
            all_files.append(filename)
    return all_files

 
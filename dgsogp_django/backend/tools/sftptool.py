import paramiko
from stat import S_ISDIR
import os

def getSftpClient(wserver):
    #密钥登录
    privage_key = paramiko.RSAKey.from_private_key_file('./ssh-key/hadoop_cluster')
    t=paramiko.Transport((wserver, 22))#ftp
    t.connect(username = 'root',pkey=privage_key)
    SftpClient = paramiko.SFTPClient.from_transport(t)
    return SftpClient

def getAllFilesInRemoteDir(sftp, remote_dir):
    # 保存所有文件的列表
    all_files = list()
    # 去掉路径字符串最后的字符'/'，如果有的话
    if remote_dir[-1] == '/':
        remote_dir = remote_dir[0:-1]
    # 获取当前指定目录下的所有目录及文件，包含属性值
    files = sftp.listdir_attr(remote_dir)
    for x in files:
        # remote_dir目录中每一个文件或目录的完整路径
        filename = remote_dir + '/' + x.filename
        # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
        if S_ISDIR(x.st_mode):
            all_files.extend(getAllFilesInRemoteDir(sftp, filename))
        else:
            all_files.append(filename)
    return all_files


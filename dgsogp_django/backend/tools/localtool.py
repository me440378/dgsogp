import os
import shutil

def makeLocalPath(localPath):
    if os.path.exists(localPath):
        return
    else:
        os.makedirs(localPath, mode=0o0775, exist_ok = True)

def makeSureLocalFile(File):
	return os.path.exists(File)

def deleteFileOrDir(PathToDelete):
    if os.path.isdir(PathToDelete):
        paths = os.listdir(PathToDelete)
        for p in paths:
            filePath = os.path.join(PathToDelete, p)
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath,True)
        os.rmdir(PathToDelete)
    else:
    	os.remove(PathToDelete)



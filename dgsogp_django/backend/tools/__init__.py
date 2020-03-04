from .hash import *
from .reply import *
from .sftp import *
import os

def makeSureLocalFile(File):
	return os.path.exists(File)
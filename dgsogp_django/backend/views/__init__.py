from django.http import HttpResponse

from .UsersView import *
from .DatasourcesView import *
from .HadoopsourcesView import *
from .MetadataView import *

def index(request):
    return HttpResponse("WoW! Here is index,in backend/views/__init__.py!")

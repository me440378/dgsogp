from django.http import HttpResponse

from .UsersView import *
from .DatasourcesView import *
from .HadoopsourcesView import *
from .MetadataView import *
from .DatainterfacesView import *
from .DatabaseinterfacesView import *
#前端视图
from .FrontendView import *

def index(request):
    return HttpResponse("WoW! Here is index,in backend/views/__init__.py!")

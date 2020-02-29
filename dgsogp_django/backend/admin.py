from django.contrib import admin

from backend.models import Datasources
from backend.models import Hadoopsources
from backend.models import Metadata
from backend.models import Users

admin.site.register(Datasources)
admin.site.register(Hadoopsources)
admin.site.register(Metadata)
admin.site.register(Users)
from django.contrib import admin
from blog.models import *

admin.site.register(CustomUser)
admin.site.register(UserNews)
admin.site.register(Comment)

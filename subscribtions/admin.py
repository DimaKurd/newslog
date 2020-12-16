from django.contrib import admin
from dal import autocomplete
from django import forms
from subscribtions.models import *


admin.site.register([BlogSubs, NewsSubs])

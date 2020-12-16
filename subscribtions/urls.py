from django.urls import path
from subscribtions.views import *

app_name = 'subscribtions'
urlpatterns = [
    path('', getAvailableData, name='getSubs'),
    path('updateNews', updateNewsSources, name='updateNews'),
    path('updateBlogs', updateBlogsSources, name='updateBlogs')
]
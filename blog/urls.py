from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('registration', views.Registration.as_view(), name='registration'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('<int:pk>/edit', views.PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete', views.delete_post, name='delete_post'),
    path('', views.show_intro, name='intro'),
    path('<int:pk>/wall', views.Wall.as_view(), name='wall'),
    path('<int:pk>/news', views.get_news_source_wall, name='get_news_wall'),
    path('feed', views.get_feed_wall, name='get_feed'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('<int:pk>/comment', views.add_comment, name='comment'),
    path('<int:pk>/del_comment', views.del_comment, name='delete_comment')
]

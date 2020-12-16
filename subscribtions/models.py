from django.db import models
from blog.models import CustomUser
from rssCollector.models import NewsSrc


class BlogSubs(models.Model):
    user_src = models.ForeignKey(related_name='source', null=True, to=CustomUser, on_delete=models.SET_NULL)
    user_rcv = models.ForeignKey(related_name='receiver', null=True, to=CustomUser, on_delete=models.SET_NULL)

    def __str__(self):
        return ' '.join([self.user_src.username, self.user_rcv.username])


class NewsSubs(models.Model):
    user = models.ForeignKey(null=True, to=CustomUser, on_delete=models.SET_NULL)
    src = models.ForeignKey(null=True, to=NewsSrc, on_delete=models.SET_NULL)

    def __str__(self):
        return ' '.join([self.user.username, self.src.name])

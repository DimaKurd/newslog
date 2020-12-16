from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, max_length=1024)
    bio = models.TextField(null=True, default='')
    pass


class UserNews(models.Model):
    src = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    header = models.CharField(max_length=256, default='Heading')
    body = models.TextField()
    picture = models.ImageField(upload_to='userpic/', null=True, max_length=1024)
    publish_date = models.DateTimeField()

    def __str__(self):
        return self.src.username + self.publish_date.__str__()

    def get_comments(self):
        try:
            comments = Comment.objects.filter(post=self).order_by('date')

            return comments
        except:
            return None

    def get_absolute_url(self):
        return reverse('blog:wall')


class Comment(models.Model):
    post = models.ForeignKey(to=UserNews, on_delete=models.CASCADE)
    body = models.TextField()
    owner = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return ' '.join([self.post.header, self.body])

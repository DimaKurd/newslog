from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class NewsSrc(models.Model):
    name = models.TextField(unique=True)
    link = models.URLField()
    descr = models.TextField(null=True)
    type = models.ForeignKey(to=Type, on_delete=models.SET_NULL, null=True)
    icon = models.URLField(default='')

    def __str__(self):
        return self.name


class WebNews(models.Model):
    src = models.ForeignKey(to=NewsSrc, on_delete=models.CASCADE)
    header = models.CharField(max_length=256, default='Heading')
    body = models.TextField(default='', null=True)
    picture = models.URLField(null=True)
    publish_date = models.DateTimeField()
    link = models.TextField(default='')

    def __str__(self):
        return ' '.join([self.src.name, str(self.publish_date)])

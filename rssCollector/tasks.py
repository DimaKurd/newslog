from datetime import datetime, timezone, timedelta

from background_task import background
from .models import *
import feedparser
from django.utils.timezone import now


@background(schedule=0)
def collectSomeRss():
    sources = NewsSrc.objects.all()
    for source in sources:
        channel = feedparser.parse(source.link)
        news = channel.entries
        queryset = WebNews.objects.filter(src_id=source.id).order_by('-publish_date')
        if len(queryset) > 0:
            last_date = queryset[0].publish_date
        else:
            last_date = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=0)))
        for item in news:
            try:
                published_date = datetime(*item.published_parsed[:6], tzinfo=timezone(timedelta(hours=item.published_parsed[-1])))
            except:
                continue
            if last_date < published_date:
                try:
                    picture = item.enclosures[0]['href']
                    if picture[-3:] == 'mp4':
                        picture = None
                except:
                    picture = None
                try:
                    description = item.description
                except:
                    continue
                new_event = WebNews(src=source, header=item.title, body=description, picture=picture, publish_date=published_date, link=item.link)
                new_event.save()

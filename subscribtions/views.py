from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from rssCollector.models import Type
from .models import *
from django.http import HttpResponseRedirect


@login_required
def getAvailableData(request):
    news_srcs = NewsSrc.objects.all()
    blog_srcs = list(CustomUser.objects.all())
    news_subs = NewsSubs.objects.filter(user=request.user)
    blog_subs = BlogSubs.objects.filter(user_rcv=request.user)

    blog_srcs.remove(request.user)
    labels = [item.src.name for item in news_subs]
    usernames = [item.user_src.username for item in blog_subs]

    types = Type.objects.order_by('name')

    success = request.session.get('success', False)
    request.session['success'] = False
    context = {'news_srcs': news_srcs,
               'news_subs': labels,
               'blog_srcs': blog_srcs,
               'blog_subs': usernames,
               'types': types,
               'success': success,
               'small': 'подписки'}
    return render(request, 'subscribtions/subscribtions.html', context)


@login_required
def updateNewsSources(request):
    source_labels = dict(request.POST)
    source_labels = list(source_labels.keys())
    source_labels.remove('csrfmiddlewaretoken')
    source_labels.remove('news_sources_length')
    try:
        newsSubs = NewsSubs.objects.filter(user=request.user)
        for subs in newsSubs:
            subs.delete()
    finally:
        for label in source_labels:
            news_source = NewsSrc.objects.get(name=label)
            NewsSubs.objects.create(user=request.user, src=news_source)
    request.session['success'] = True
    return HttpResponseRedirect(reverse('subscribtions:getSubs'))


@login_required
def updateBlogsSources(request):
    source_labels = dict(request.POST)
    source_labels = list(source_labels.keys())
    source_labels.remove('csrfmiddlewaretoken')
    source_labels.remove('blog_sources_length')
    try:
        blogsSubs = BlogSubs.objects.filter(user_rcv=request.user)
        for subs in blogsSubs:
            subs.delete()
    finally:
        for name in source_labels:
            source_user = CustomUser.objects.get(username=name)
            BlogSubs.objects.create(user_src=source_user, user_rcv=request.user)
    request.session['success'] = True
    return HttpResponseRedirect(reverse('subscribtions:getSubs'))

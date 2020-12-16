import os
import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.core.paginator import Paginator

from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from django.contrib.auth import authenticate, login, logout

from NewsBlog.storage_backends import MediaStorage
from .models import *
from rssCollector.models import *
from subscribtions.models import *


class Registration(View):

    def get(self, request):
        context = {'reg_stat': 1,
                   'small': 'регистрация'}
        return render(request, 'blog/registration.html', context)

    def post(self, request):
        try:
            user = CustomUser.objects.create_user(username=request.POST['username'],
                                                  email=request.POST['email'],
                                                  password=request.POST['password1'])
        except IntegrityError:
            context = {'reg_stat': 0}
            return render(request, 'blog/registration.html', context)
        request.session['reg_stat'] = 1
        return HttpResponseRedirect(reverse('blog:login'))


class Login(View):
    def get(self, request):
        reg_status = request.session.get('reg_stat', 0)
        log_status = request.session.get('log_stat', 2)
        request.session['reg_stat'] = 0
        request.session['log_stat'] = 2
        context = {'reg_stat': reg_status,
                   'log_stat': log_status,
                   'small': 'вход'}
        return render(request, 'blog/login.html', context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['log_stat'] = 1
            return HttpResponseRedirect(reverse('blog:intro'))
        else:
            request.session['log_stat'] = 0
            return HttpResponseRedirect(reverse('blog:login'))


def get_bucket_url(filename, request):
    try:
        picture = request.FILES[filename]

        file_directory_within_bucket = 'user_upload_files/{username}'.format(username=request.user)

        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            str(uuid.uuid4())
        )

        media_storage = MediaStorage()

        if not media_storage.exists(file_path_within_bucket):  # avoid overwriting existing file
            media_storage.save(file_path_within_bucket, picture)
            file_url = media_storage.url(file_path_within_bucket)
        else:
            return JsonResponse({
                'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
                    filename=picture.name,
                    file_directory=file_directory_within_bucket,
                    bucket_name=media_storage.bucket_name
                ),
            }, status=400)
    except MultiValueDictKeyError:
        file_url = None

    return file_url


class PostUpdate(LoginRequiredMixin, View):

    def get(self, request, pk):
        post = UserNews.objects.get(pk=pk)
        return render(request,
                      'blog/UserNews_update_form.html',
                      {'post': post,
                       'user': request.user,
                       'small': 'редактирование'})

    def post(self, request, pk):
        if UserNews.objects.get(pk=pk).src.id == request.user.id:
            post = UserNews.objects.get(pk=pk)
            post.header = request.POST['header']
            post.body = request.POST['body']

            file_url = get_bucket_url('picture', request)
            if file_url is not None:
                post.picture = file_url
            post.save()

        return HttpResponseRedirect(reverse('blog:wall', args=[request.user.id]))


class Wall(LoginRequiredMixin, View):
    template_name = 'blog/wall.html'

    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        user_news = UserNews.objects.filter(src=user).order_by('-publish_date')
        owner = (user == request.user)

        paginator = Paginator(user_news, 10)
        page = request.GET.get('page')
        user_news = paginator.get_page(page)

        context = {'blogger': user,
                   'user_news': user_news,
                   'owner': owner,
                   'small': 'блог'}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        user = request.user
        if user.id == pk:
            header = request.POST['header']
            body = request.POST['body']
            publish_date = now()

            file_url = get_bucket_url('picture', request)

            UserNews.objects.create(src=user, header=header,
                                    body=body, picture=file_url, publish_date=publish_date)
            return HttpResponseRedirect(reverse('blog:wall', args=[user.id]))
        else:
            return HttpResponseRedirect(reverse('blog:intro'))


class Profile(LoginRequiredMixin, View):
    template_name = 'blog/profile.html'

    def get(self, request):
        status = 0
        if request.session.get('profile', 0) == 1:
            status = 1
            request.session['profile'] = 0
        return render(request, self.template_name, context={'user': request.user,
                                                            'status': status,
                                                            'small': 'профиль'})

    def post(self, request):
        file_url = get_bucket_url('avatar', request)
        password = request.POST['password1']
        bio = request.POST['bio']

        user = CustomUser.objects.get(pk=request.user.id)
        if file_url is not None:
            user.avatar = file_url
        user.bio = bio
        if password != '':
            user.set_password(password)
            user.save()
            request.session['password'] = 1
            return HttpResponseRedirect(reverse('blog:intro'))
        else:
            user.save()
            request.session['profile'] = 1
            return HttpResponseRedirect(reverse('blog:profile'))


@login_required
def delete_post(request, pk):
    post = UserNews.objects.get(pk=pk)
    post.delete()
    return HttpResponseRedirect(reverse('blog:wall', args=[request.user.id]))


def show_intro(request):
    log_stat = request.session.get('log_stat', 2)
    request.session['log_stat'] = 2
    pass_stat = request.session.get('password', 2)
    request.session['password'] = 2
    news_srs = NewsSrc.objects.order_by('name')
    context = {'log_stat': log_stat,
               'password': pass_stat,
               'user': request.user,
               'news_srs': news_srs,
               'small': 'старт'}
    return render(request, 'blog/intro.html', context)


@login_required
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:login'))


def get_news_source_wall(request, pk):
    news = WebNews.objects.filter(src_id=pk).order_by('-publish_date')
    source = NewsSrc.objects.get(pk=pk)
    paginator = Paginator(news, 20)
    page = request.GET.get('page')
    news = paginator.get_page(page)
    context = {'news': news,
               'source': source,
               'small': source.name}
    return render(request, 'blog/news_source_wall.html', context=context)


def parse_news(query, content_type):
    feed = []
    for item in query:
        t = dict()
        t['id'] = item.id
        t['header'] = item.header
        t['body'] = item.body
        t['src'] = item.src
        t['picture'] = item.picture
        if content_type == 0:
            t['link'] = None
            t['comments'] = item.get_comments()
        else:
            t['link'] = item.link

        t['publish_date'] = item.publish_date
        t['type'] = content_type
        feed.append(t)

    return feed


@login_required
def get_feed_wall(request):
    blog_subs = BlogSubs.objects.filter(user_rcv=request.user)
    news_subs = NewsSubs.objects.filter(user=request.user)

    blogers = [item.user_src for item in blog_subs]
    news_src = [item.src for item in news_subs]

    blog_news = UserNews.objects.filter(src__in=blogers).order_by('-publish_date')
    web_news = WebNews.objects.filter(src__in=news_src).order_by('-publish_date')

    feed = parse_news(blog_news, 0) + parse_news(web_news, 1)
    feed = sorted(feed, key=lambda x: x['publish_date'], reverse=True)
    paginator = Paginator(feed, 20)
    page = request.GET.get('page')
    feed = paginator.get_page(page)

    return render(request, 'blog/newsFeed.html', context={'feed': feed,
                                                          'small': 'персональная лента'})


@login_required
def add_comment(request, pk):
    post = UserNews.objects.get(pk=pk)
    owner = request.user
    body = request.POST['body']
    Comment.objects.create(post=post, body=body, owner=owner, date=now())
    whereto = request.POST['next']
    page = request.POST['page']
    return HttpResponseRedirect(whereto + '?page=' + str(page))


@login_required
def del_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    whereto = request.POST['next']
    return HttpResponseRedirect(whereto)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import logout as auth_logout
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from social_django.models import UserSocialAuth
from django.http.response import HttpResponse
import requests

def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', {'posts': posts})

def logout(request):
    auth_logout(request)
    return redirect('/')

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})



def home(request):
    #  r = requests.put('http://httpbin.org/put', data = {'key':'value'})
    #  r = requests.delete('http://httpbin.org/delete')
    #  r = requests.head('http://httpbin.org/get')
    #  r = requests.options('http://httpbin.org/get')


    token = request.user.social_auth.get(
        provider=request.session.get('social_auth_last_login_backend')
    ).access_token

    provider = request.session.get('social_auth_last_login_backend')
    if provider == 'eventbrite':
        me = requests.get('https://www.eventbriteapi.com/v3/users/me/?token='+token)
        events = requests.get('https://www.eventbriteapi.com/v3/users/me/owned_events/?token='+token)
        i = 0
        lista = []
        for event in events.json()['events']:
            lista.append(event['name']['text'])
    else:
        me = ''
        events = ''
        lista = []



    ctx = {
        'provider': provider,
        'key': request.session.get('key'),
        'hash': request.session.get('_auth_user_hash'),
        'id': request.user.social_auth.get(provider=request.session.get('social_auth_last_login_backend')).uid,
        'backend': request.session.get('_auth_user_backend'),
        'token': token,
        'events': lista,

    }


    if request.user.is_authenticated():
        return render(request, 'blog/home.html',{'ctx': ctx,'r':me,})


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})

def profile(request):

    return render(request,'profile.html',{'form': ''})


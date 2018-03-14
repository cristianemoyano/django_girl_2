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
    all_entries = UserSocialAuth.objects.all()
    user = UserSocialAuth.objects.get(pk=1)

    if request.user.is_authenticated():
        return render(request, 'blog/home.html',{'all_entries': all_entries})

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


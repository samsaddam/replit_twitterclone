# from typing_extensions import Required
from django import forms
from django.http.response import HttpResponseBase, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
# from django.urls import reverse_lazy, reverse
# from cloudinary.forms import cl_init_js_callbacks
# Create your views here.


def index(request):
    # if the method is POST
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        img = PostForm(request.FILES)
        print(form)
    # If the form is valid
        if form.is_valid():
            form.image = img
            #yes, save
            form.save()
          # Redirect to home
            return HttpResponseRedirect('/')

        else:
            # no, Show Error
            return HttpResponseRedirect(form.errors.as_json())

    # Get all posts, limit = 20
    posts = Post.objects.all().order_by('-created_at')[:20]
    form = PostForm()
    # Show
    return render(request, 'posts.html', {'posts': posts})


def delete(request, post_id):
    # Find post
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')


def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect(form.errors.as_json())
    return render(request, 'edit.html', {'post': post})


def like(request, post_id):
    post = Post.objects.get(id=post_id)
    newlikecount = post.like_count+1
    post.like_count = newlikecount
    post.save()
    return HttpResponseRedirect('/')

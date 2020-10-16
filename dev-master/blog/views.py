from django.shortcuts import render, redirect

from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.forms.models import model_to_dict
import json
from .models import *

def Blog_Main_View(request):
    template_name="blog/blog.html"
    context={
        'posts' : blogPost.objects.all()
    }
    return render(request, template_name, context)

def post_details_view(request, post_id):
    template_name="blog/blog-post.html"
    context={
        'post' : blogPost.objects.get(id=post_id)

    }
    return render(request, template_name, context)

def post_details_by_slug_view(request, slug):
    template_name="blog/blog-post.html"
    context={
        'post' : blogPost.objects.get(slug=slug)
    }
    return render(request, template_name, context)

def search_view(request):
    template_name="blog/blog-search.html"
    if request.method == "GET":
        context={
            'records' : None
        }
        return render(request,template_name, context)
    else:
        if request.POST['search'].strip() != '':
            context={
                'search_string' :request.POST['search'],
                'records' : blogPost.objects.filter(title__icontains = request.POST['search'])
            }
            return render(request,template_name, context)
        else:
            context={
                'records' : None
            }
            return render(request,template_name, context)

def postCommentView(request, slug):
    if request.user.is_authenticated:
        if request.is_ajax and request.method == "POST":
            try:
                post = blogPost.objects.get(slug=slug)
                comment = postComment.objects.create(
                    user = request.user,
                    post = post,
                    body = request.POST['comment']
                )
                comment.save()
                context = {
                    'comment' : comment,
                    'post' : post
                }
                return render(request, "blog/comment_content.html", context)
            except Exception as e:
                print(e)
                return JsonResponse({"error": "Invalid post for a comment" }, status=400)
        else:
            return JsonResponse({"error": "Invalid Request" }, status=400)
    else:
        return JsonResponse({"error": "You need to login" }, status=400)

@login_required
def commentReplyView(request, slug, comment_id):
    try:
        post = blogPost.objects.get(slug= slug)
        comment = postComment.objects.get(id=comment_id)
        commentReply.objects.create(
            user = request.user,
            post = post,
            comment = comment,
            body = request.POST['reply']
        )
        return redirect(post.get_absolute_url())
    except Exception as e:
        print(e)
        return redirect(reverse("Blog_Main_Page"))
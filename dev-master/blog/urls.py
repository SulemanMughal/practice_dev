from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Blog_Main_View, name="Blog_Main_Page"),
    path('post/<int:post_id>', views.post_details_view, name="post_detail_page"),
    path('post/<str:slug>', views.post_details_by_slug_view, name="post_detail_page_by_slug"),
    path('search', views.search_view, name='search_page'),
    
    # submit a post comment
    path('post/<str:slug>/comment', views.postCommentView, name="post_comment_url"),

    # submit a comment reply
    path('post/<str:slug>/comment/<int:comment_id>/reply', views.commentReplyView, name="comment_reply_url"),
]
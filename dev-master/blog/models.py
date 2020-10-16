from django.db import models
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.urls import reverse

class blogPost(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="Post Title", default="Post Title",  blank=False, null=False)
    slug = models.SlugField(verbose_name="Post Title Slugified", blank=False, null=False, default='')
    body = RichTextUploadingField(blank=True)
    publish = models.BooleanField(verbose_name="Post Publish Status", default=False, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'slug' : self.slug
        }
        return reverse('post_detail_page_by_slug', kwargs=kwargs)

    def get_published_comments(self):
        return self.postcomment_set.all().filter(publish = True)

class postComment(models.Model):
    user  = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(blogPost, on_delete=models.CASCADE)
    body = models.TextField(verbose_name="Comment Body", blank=False,  null=False, default ="")
    publish = models.BooleanField(verbose_name="Commet Publish Status", default=True, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True )


    class Meta:
        ordering = [
            'timestamp'
        ]


    def __str__(self):
        return self.post.title

    def get_published_reply(self):
        return self.commentreply_set.all().filter(publish = True)


class commentReply(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(blogPost, on_delete=models.CASCADE)
    comment = models.ForeignKey(postComment, on_delete=models.CASCADE)
    body = models.TextField(verbose_name="Reply Body", blank=False, null=False, default="")
    publish = models.BooleanField(verbose_name="Reply Publish Status", default=True, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            'timestamp'
        ]

    def __str__(self):
        return self.post.title
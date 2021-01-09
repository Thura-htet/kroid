from datetime import timedelta

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

from django.db import models
from django.db.models import F, Q
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

User = settings.AUTH_USER_MODEL

markdown = mistune.Markdown()


class PostQuerySet(models.QuerySet):
    def feed(self, user):
        followed_users_id = []
        if user.following.exists():
            followed_users_id = user.following.values_list('user_id', flat=True)
        return self.filter(
            Q(author__id__in=followed_users_id) | Q(author=user)
        ).distinct().order_by('-timestamp')


class PostManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PostQuerySet(model=self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)


class Post(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    author_name = models.CharField(null=False, max_length=12)
    title = models.CharField(max_length=128, null=False, blank=False)
    summary = models.CharField(max_length=256, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    html_content = models.TextField(blank=True)
    # if i'm keeping comment_count maybe i should also keep view_count?
    comment_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    # gonna keep the same lenght as title for now
    slug = models.SlugField(null=True)

    objects = PostManager()

    class Meta:
        # probably should not order by anything at all
        ordering = ['timestamp']

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if self.content and not self.html_content:
    #         html = markdown(self.content)
    #         self.html_content = html
            
    #     if self.pk and not self.slug:
    #         masked_id = self.id ^ 0xABCDEF # until there is a proper hash function
    #         slug = f"{self.title} {masked_id}"
    #         self.slug = slugify(slug, allow_unicode=True)
    #         ViewCount.objects.create(viewed_post=self)
    #     super(Post, self).save(*args, **kwargs)


class Comment(MPTTModel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    author_name = models.CharField(null=False, max_length=12)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='children', 
        db_index=True)
    comment = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    class MPTTMeta:
            order_insertion_by = ['timestamp']
    def delete(self, *args, **kwargs):
        parent_post = Post.objects.get(id=self.parent_post)
        parent_post.comment_count -= 1
        parent_post.save()
        super(Comment, self).delete()
    @property
    def is_child(self):
        return self.parent != None
    def __str__(self):
        return self.comment


class ViewCount(models.Model):
    viewed_post = models.OneToOneField(Post, on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)
    def increase(self):
        # why not += 1
        self.view_count = F('view_count')+1
        self.save()
    def decrease(self):
        # why not -= 1
        self.view_count = F('view_count')-1
        self.save()
    def views_in_last(self, **kwargs):
        assert kwargs, "Must provide at least one timedelta arg (eg: days=1)"
        period = timezone.now() - timedelta(**kwargs)
        return self.view_set.filter(created__gte=period).count()


class View(models.Model):
    # should save viewed post
    created = models.DateTimeField(auto_now_add=True, editable=False)
    ip = models.CharField(max_length=40, editable=False, null=True, blank=True)
    session = models.CharField(max_length=40, editable=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    counter = models.ForeignKey(ViewCount, editable=False, on_delete=models.CASCADE) # referenced by view_set
    def save(self, *args, **kwargs):
        if self.pk is None:
            ViewCount.objects.get(pk=self.counter.pk).increase()
        super(View, self).save(*args, **kwargs)
    def delete(self, save_count=True):
        if not save_count:
            ViewCount.objects.get(pk=self.counter.pk).decrease()
        super(View, self).delete()


@receiver(post_save, sender=Post)
def post_did_save(sender, instance, created, *args, **kwargs):
    if created:
        ViewCount.objects.create(viewed_post=instance)
        if instance.pk and not instance.slug:
            masked_id = instance.id ^ 0xABCDEF # until there is a proper hash function
            slug = f"{instance.title} {masked_id}"
            instance.slug = slugify(slug, allow_unicode=True)
            instance.save()

@receiver(pre_save, sender=Post)
def post_will_save(sender, instance, *args, **kwargs):
    if instance.content and not instance.html_content:
            html = markdown(instance.content)
            instance.html_content = html

@receiver(post_save, sender=Comment)
def comment_did_save(sender, instance, created, *args, **kwargs):
    if created:
        parent_post = Post.objects.get(id=instance.parent_post.id)
        parent_post.comment_count += 1
        parent_post.save()

from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

User = settings.AUTH_USER_MODEL

    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=128, null=False, blank=False)
    summary = models.CharField(max_length=256, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    view_count = models.IntegerField(default=0)
    argument_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    # gonna keep the same lenght as title for now
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id:
            masked_id = self.id ^ 0xABCDEF # until there is a proper hash function
            slug = f"{self.title} {masked_id}"
            self.slug = slugify(slug, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)


class Comment(MPTTModel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, 
    null=True, blank=True, related_name='children', 
    db_index=True)
    comment = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
            order_insertion_by = ['timestamp']
            
    @property
    def is_child(self):
        return self.parent != None

    def __str__(self):
        return self.comment


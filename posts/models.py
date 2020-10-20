from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey

User = settings.AUTH_USER_MODEL

    
class Post(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=128, null=False, blank=False)
    summary = models.CharField(max_length=256, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    view_count = models.IntegerField(default=0)
    argument_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return self.title
    
    @property
    def post_url(self):
        return f"/post/{self.id}"

    @property
    def author_url(self):
        return f"/user/{self.author}"

class Comment(MPTTModel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = TreeForeignKey('self', on_delete=models.SET_NULL, 
    null=True, blank=True, related_name='children', 
    db_index=True)
    comment = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
            order_insertion_by = ['timestamp']
            
    @property
    def is_child(self):
        return self.parent_comment != None

    def __str__(self):
        return self.parent_comment


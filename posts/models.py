from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# add a serialize function and class Meta: ordering=[-id] and migrate
class Post(models.Model):
    # user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) <<< this deletes the user but not the posts
    user = models.ForeignKey(User, on_delete=models.CASCADE) # for now if a user is deleted all of his posts are also deleted
    title = models.CharField(max_length=128, null=False, blank=False)
    summary = models.CharField(max_length=256, null=False, blank=False)
    content = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ['-id']

    # def __str__(self):
    #     return self.title
    
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "content": self.content
        }
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pen_name = models.CharField(max_length=32, null=True, blank=True)
    bio = models.TextField(max_length=256, null=True, blank=True)
    fav_quote = models.TextField(max_length=256, null=True, blank=True)
    # there will be:
    # a team(probably ForeignKey or OneToMany),
    # interests(Choice)


@receiver(post_save, sender=User)
def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
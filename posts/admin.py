from django.contrib import admin

# Register your models here.

from .models import Post, PostLike, Comment

class PostLikeAdmin(admin.TabularInline):
    model = PostLike

class PostAdmin(admin.ModelAdmin):
    inlines = [PostLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['user__username']
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
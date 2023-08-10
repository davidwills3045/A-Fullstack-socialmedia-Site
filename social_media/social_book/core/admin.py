from django.contrib import admin
from .models import Profile,Post,likePost,followersCount

# class MemberAdmin(admin.ModelAdmin):
#     list_display = ()

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(likePost)
admin.site.register(followersCount)
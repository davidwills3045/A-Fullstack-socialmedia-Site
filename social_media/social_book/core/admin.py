from django.contrib import admin
from .models import Profile,Post

# class MemberAdmin(admin.ModelAdmin):
#     list_display = ()

admin.site.register(Profile)
admin.site.register(Post)
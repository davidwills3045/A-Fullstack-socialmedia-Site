from django.contrib import admin
from .models import Profile

# class MemberAdmin(admin.ModelAdmin):
#     list_display = ()

admin.site.register(Profile)
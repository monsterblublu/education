from django.contrib import admin
from .models import Group, GroupMember, Post
# Register your models here.


class MemberInline(admin.TabularInline):
    model = GroupMember

class PostInline(admin.TabularInline):
    model = Post

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name','created_by')
    actions = None

    inlines = [
        MemberInline,
        PostInline,
    ]

admin.site.register(Group, GroupAdmin)

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(allow_unicode=True, unique=True)
    token = models.CharField('join token', max_length=6, unique=True)
    description = models.TextField(blank=True, default='')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     through="GroupMember")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='CreatorGroups',
                                   related_query_name='creator',
                                   on_delete=models.CASCADE,
                                   null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = get_random_string(length=16)
        self.token = get_random_string(length=6)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        reverse('groups:detail', kwargs={'slug':self.slug})

    class Meta:
        verbose_name = 'group chat'
        verbose_name_plural = 'group chats'

class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name="memberships",
                              on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="user_groups",
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + self.user.last_name

    class Meta:
        unique_together = ('group', 'user')
        verbose_name = 'group member'
        verbose_name_plural = 'group members'


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    group = models.ForeignKey(Group, related_name="post",
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ["-created_at"]
        unique_together = ('user', 'message')

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView,ListView,
                                  DetailView, RedirectView)
from django.db import IntegrityError
from .models import Group, GroupMember, Post
from django.urls import reverse
from django.contrib import messages
# Create your views here.


class CreateGroup(LoginRequiredMixin, CreateView):
    model = Group
    fields = ('name', 'description')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)



class ListGroup(LoginRequiredMixin, ListView):
    model = Group

class DetailGroup(LoginRequiredMixin, DetailView):
    model = Group

class JoinGroup(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, "Sudah bergabung di {}".format(group.name))
        else:
            messages.success(self.request, "Berhasil bergabung di {}".format(group.name))
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:detail', slug=self.kwargs.get('slug'))


class LeaveGroup(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(
                group__slug=self.kwargs.get('slug'),
                user=self.request.user
                ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request, "Anda tidak dapat keluar karena anda belum bergabung")
        else:
            membership.delete()
            messages.success(self.request, "Anda berhasil keluar")
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:detail', slug=self.kwargs.get('slug'))

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('message')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.group = self.request.group
        self.object.save()
        return super().form_valid(form)


class ListPost(ListView):
    model = Post


class DetailPost(LoginRequiredMixin, DetailView):
    model = Post






# created by Chirath R, chirath.02@gmail.com
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300)
    url = models.URLField(max_length=400, null=True, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.created_by.username + ' ' + self.title

    def get_absolute_url(self):
        return " "


class ProjectImages(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project/')

    def __str__(self):
        return self.project


class ProjectMembers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_assigned = models.DateTimeField(auto_now_add=True, auto_now=False)


class Language(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)





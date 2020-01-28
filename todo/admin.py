from django.contrib import admin
from .models import Project,Outline,Task,Profile

admin.site.register(Project)
admin.site.register(Outline)
admin.site.register(Task)
admin.site.register(Profile)
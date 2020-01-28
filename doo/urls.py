from django.conf.urls import url
from django.contrib.auth import views as djangos
from django.contrib import admin
from django.conf.urls import include
from django.urls import path

#from django.urls import path

from todo import views as todo
from accounts import views as auth

urlpatterns = [
    url(r'^$', todo.home, name='home'),
    url(r'^home/$', todo.home, name='home'),
    url(r'^signup/$',auth.signup,name='signup'),
    url(r'^login/$',auth.login,name="login"),
    url(r'^password/$',auth.password,name="password"),
    url(r'^logout/$',djangos.LogoutView.as_view(),name="logout"),
    url(r'^profile/$',auth.profile,name="profile"),
    url(r'^edit-profile/$',auth.edit_profile,name="edit-profile"),
    url(r'^project/(\d+)/$', todo.project, name='project'), 
    url(r'^outline/(\d+)/$', todo.outline, name='outline'), 
    url(r'^finished/$', todo.finished, name='finished'), 
    url(r'^urgent/$', todo.urgent, name='urgent'),  
    url(r'^week/$', todo.week, name='week'),         
    url(r'^new-outline/$', todo.new_outline, name='new-outline'),
    url(r'^new-project/$', todo.new_project, name='new-project'),
    url(r'^new-task/$', todo.new_task, name='new-task'),
    url(r'^finish-task/$', todo.finish_task, name='finish-task'),
    url(r'^restore-task/$', todo.restore_task, name='restore-task'),
    url(r'^delete-task/$', todo.delete_task, name='delete-task'),
    url(r'^admin/', admin.site.urls),
]

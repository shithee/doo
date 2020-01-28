from django.urls import reverse
from django.urls import resolve
from django.test import TestCase

from .views import home,project
from .models import Project

class Hometests(TestCase):

    def test_home_status(self):
        url= reverse('home')
        res= self.client.get(url)
        self.assertEquals(res.status_code,200)
    
    def test_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func,home)

class Projecttests(TestCase):

    def test_project_view(self):
        view = resolve('/')
        self.assertEquals(view.func,project)


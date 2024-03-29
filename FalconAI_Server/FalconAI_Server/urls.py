"""FalconAI_Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from email_generator import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("send/email", views.sendEmail, name="send email"),
    path("generate/email", views.generateEmail, name="generate email"),
    path("store/email", views.storeEmail, name="store email"),
    path("fetch/email", views.fetchEmail, name="fetch email"),
    path("schedule/email", views.scheduleEmail, name="schedule email"),
    path("click/email", views.clickEmail, name="Click email"),
    path("create/employee", views.createEmployee, name="Create Employee"),
    path("create/business", views.createBusiness, name="Create Business"),
    path("create/admin", views.createAdmin, name="Create Admin"),
]

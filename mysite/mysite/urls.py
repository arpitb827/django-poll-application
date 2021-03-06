"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include,path
from Events.admin import event_admin_site
from Entities.admin import entity_admin_site
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [

    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    # path('', include('polls.urls')),
    path('', include('dear_diary.urls')),
    path('entity-admin/', entity_admin_site.urls),
    path('event-admin/', event_admin_site.urls),
    


]

urlpatterns += staticfiles_urlpatterns()

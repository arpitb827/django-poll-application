from django.urls import path

from . import views

app_name = 'dear_diary'

urlpatterns = [
   path('', views.index, name="home"),
   path('add/', views.add, name="add")

]
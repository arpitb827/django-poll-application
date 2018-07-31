from django.shortcuts import render

from django.views.generic import TemplateView, ListView, CreateView
from .models import Promise
# Create your views here.

class PromiseCreateView(CreateView):
    model = Promise
    form_class = PromiseForm
from django.shortcuts import render, redirect
from .models import Entry
# Create your views here.
from .forms import EntryForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def index(request):
	# entries = Entry.objects.all()
	entries = Entry.objects.order_by('-pub_date')

	context= {'entries':entries}
	return render(request,'dear_diary/diary.html', context)

def add(request):
	if request.method == 'POST':
		form = EntryForm(request.POST)
		if form.is_valid():
			form.save()
			# return HttpResponseRedirect(reverse('dear_diary:home'))
			return redirect('dear_diary:home')
	else:
		form = EntryForm()
	context = {'form': form}
	return render(request,'dear_diary/add_entry.html', context)

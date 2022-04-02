# abstract_match/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .forms import AbstractForm


class HomePageView(TemplateView):
	template_name = 'home.html'

def get_abstract(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AbstractForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/results/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AbstractForm()

    return render(request, 'home.html', {'form': form})

class ResultsView(TemplateView):
	template_name = 'results.html'

	def post(self, request):
		context = {}
		context["user_abstract"] = request.POST['user_abstract']
		return render(request, 'results.html', context)

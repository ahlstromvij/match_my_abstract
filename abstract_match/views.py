# abstract_match/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .forms import AbstractForm
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.templatetags.static import static
import os
from django.conf import settings


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

		file = open(os.path.join(settings.STATIC_ROOT, 'csv/arxiv_df.csv'))
		df_clean = pd.read_csv(file)
		context["csv"] = df_clean['journal'][0]

		return render(request, 'results.html', context)

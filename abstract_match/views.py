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

		documents = []
		for index, row in df_clean[["abstract"]].iterrows():
			documents.append(row.to_string()[12:])

		input_doc = request.POST['user_abstract']
		documents.append(input_doc)
		vect = TfidfVectorizer(min_df=1, stop_words="english")  
		tfidf = vect.fit_transform(documents)
		pairwise_similarity = tfidf * tfidf.T
		df2 = pd.DataFrame(data=pairwise_similarity.toarray())
		similarity = df2.loc[len(df2)-1]
		similarity.pop(len(df2)-1)
		df_clean['similarity'] = similarity

		all_journals = df_clean['journal'].unique()
		d = []
		for j in all_journals:
			d.append(
				{
					'Journal': j,
					'Similarity': df_clean.loc[df_clean['journal'] == j, 'similarity'].mean(),
				}
			)

		similarity_df = pd.DataFrame(d)
		similarity_df.Similarity = pd.to_numeric(similarity_df.Similarity, errors='coerce')
		similarity_df_sorted = similarity_df.sort_values(by='Similarity', ascending=False)
		similarity_df_sorted = similarity_df_sorted.reset_index(drop=True)

		context["match1_journal"] = similarity_df_sorted['Journal'][0]
		context["match2_journal"] = similarity_df_sorted['Journal'][1]
		context["match3_journal"] = similarity_df_sorted['Journal'][2]
		context["match4_journal"] = similarity_df_sorted['Journal'][3]
		context["match5_journal"] = similarity_df_sorted['Journal'][4]

		context["match1_similarity"] = round(similarity_df_sorted['Similarity'][0],2)
		context["match2_similarity"] = round(similarity_df_sorted['Similarity'][1],2)
		context["match3_similarity"] = round(similarity_df_sorted['Similarity'][2],2)
		context["match4_similarity"] = round(similarity_df_sorted['Similarity'][3],2)
		context["match5_similarity"] = round(similarity_df_sorted['Similarity'][4],2)

		return render(request, 'results.html', context)

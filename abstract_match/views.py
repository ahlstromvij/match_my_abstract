# abstract_match/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .forms import AbstractForm
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from django.conf import settings


class HomePageView(TemplateView):
	template_name = 'home.html'

class AboutPageView(TemplateView):
	template_name = 'about.html'

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

		num_matches = similarity_df_sorted['Similarity'][similarity_df_sorted['Similarity'] != 0].count()
		context["num_matches"] = num_matches

		keys = similarity_df_sorted['Journal'][0:5]
		values = round(similarity_df_sorted['Similarity'][0:5],2)
		match_dict = dict(zip(keys, values))
		filtered_dict = {key: value for (key, value) in match_dict.items() if value > 0 }
		context["filtered_dict"] = filtered_dict

		return render(request, 'results.html', context)

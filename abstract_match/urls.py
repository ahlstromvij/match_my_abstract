# abstract_match/urls.py
from django.urls import path
from .import views
from .views import ResultsView, AboutPageView

urlpatterns = [
	path('', views.get_abstract, name='home'),
	path('results/', ResultsView.as_view(), name='results'),
	path('about/', AboutPageView.as_view(), name='about'),
]
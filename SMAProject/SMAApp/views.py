# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .forms import SearchForm
from SMAApp import extract, engagements
from django.template.response import TemplateResponse
# Create your views here.

def home(request):
	return get_keyword(request)

def get_keyword(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			print('extracting')
			df = extract.searchKeyWord(form.cleaned_data['keyword'])
			data = engagements.return_engagements(df)
			return render(request, 'diagnostics.html',
                 {'users': "{:,}".format(data['users']),
                  'tweets': "{:,}".format(data['tweets']),
                  'engagements': "{:,}".format(data['engagements']),
                  'reach': "{:,}".format(data['reach'])})    
	else:
		form = SearchForm()
	return render(request, 'search.html', {'form': form})

class diagnostics(TemplateView):
    template_name = "diagnostics.html"
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .forms import SearchForm
from SMAApp import extract
# Create your views here.

def home(request):
	return get_keyword(request)

def get_keyword(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			print('extracting')
			extract.searchKeyWord(form.cleaned_data['keyword'])
	else:
		form = SearchForm()
	return render(request, 'search.html', {'form': form})
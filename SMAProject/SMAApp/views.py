# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .forms import SearchForm
from SMAApp import extract, engagements
from django.template.response import TemplateResponse
import pandas as pd
# Create your views here.

def home(request):
	return get_keyword(request)

def get_keyword(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			print('extracting')
			request.session['engagements_data'] = ""
			#df = extract.searchKeyWord(form.cleaned_data['keyword'])
			df = pd.read_pickle("file.pkl")
			data = engagements.return_engagements(df)
			formattedData = formatData(data)
			all_data = {}
			all_data["engagements"] = formattedData
			request.session['engagements_data'] = all_data
			timeline = engagements.return_timeline(df)
			all_data["timeline"] = demo_linechart(request, timeline)
			return render(request, 'diagnostics.html',
                all_data)
	else:
		form = SearchForm()
	return render(request, 'search.html', {'form': form})

def open_diagnostics(request):
	formattedData = request.session['engagements_data']
	return render(request, 'diagnostics.html',
               formattedData)  
    #template_name = "diagnostics.html"

def formatData(data):
 	return	{'users': "{:,}".format(data['users']),
                  'tweets': "{:,}".format(data['tweets']),
                  'engagements': "{:,}".format(data['engagements']),
                  'reach': "{:,}".format(data['reach'])}
     
def demo_linechart(request, chartdata):
    """
    lineChart page
    """
    charttype = "lineChart"
    chartcontainer = 'linechart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '%b-%d %H:%m',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return data
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, JsonResponse
from .forms import SearchForm
from SMAApp import extract, engagements
import pandas as pd
import json
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
			sourceData = engagements.return_source(df)
			sourceFormattedData = sourcePiechartConverter(sourceFormatData(sourceData))
			all_data["source"] = sourceFormattedData
			composition = engagements.return_composition(df)
			compositionFormattedData = compositionPiechartConverter(compositionFormatData(composition))
			all_data["composition"] = compositionFormattedData
			request.session["df"] = df
			return render(request, 'diagnostics.html',
                all_data)
	else:
		form = SearchForm()
	return render(request, 'search.html', {'form': form})

def return_geocode(request):
	geoCodes = engagements.return_geocode(request.session["df"])
	return JsonResponse(geoCodes)  

def open_diagnostics(request):
	formattedData = request.session['engagements_data']
	return render(request, 'diagnostics.html',
               formattedData)  
    #template_name = "diagnostics.html"

def open_influencers(request):
	data = {}
	data = engagements.return_engagements(request.session["df"])
	data['engData'] = engagements.return_influencers(request.session["df"],'engagements')
	data['folData'] = engagements.return_influencers(request.session["df"],'flcount')
	return render(request, 'influencers.html', {'engData':data['engData'],'folData':data['folData'] })  

def open_influentialposts(request):
    data = {}
    df = pd.read_pickle("file.pkl")
    data = engagements.return_infl_posts(df)
    data["influentialPost"] = data
    return render(request, 'influentialposts.html', data)  

def open_sentiments(request):
    chartdata = engagements.return_polarity(request.session["df"])
    data = {}
    data['polar'] = demo_donutchart(chartdata)
    return render(request, 'sentiments.html', data)

def open_topics(request):
	return render(request, 'topics.html')

def formatData(data):
 	return	{'users': "{:,}".format(data['users']),
                  'tweets': "{:,}".format(data['tweets']),
                  'engagements': "{:,}".format(data['engagements']),
                  'reach': "{:,}".format(data['reach'])}

def sourceFormatData(data):
    return {'webClient': "{:,}".format(data['Web Client']),
            'android': "{:,}".format(data['Android']),
            'iPhone': "{:,}".format(data['iPhone']),
            'others': "{:,}".format(data['Others']),
            } 

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

def demo_donutchart(chartdata):
    """
    pieChart page
    """
    charttype = "pieChart"
    chartcontainer = 'piechart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
    			'donut':True,
            'donutRatio':0.5,
            'chart_attr':{
                'labelType':'\"percent\"',
            }
        }
    }
    return data

def sourcePiechartConverter(data):
    """
    pieChart page
    """
    
    xdata = ["Web Client", "Android", "iPhone", "Others"]
    ydata = [data["webClient"], data["android"], data["iPhone"], data["others"]]

    extra_serie = {"tooltip": {"y_start": "", "y_end": ""}}
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype = "pieChart"
    chartcontainer = 'source_piechart_container'

    data = {
        'chartcontainer': chartcontainer,
        'charttype': charttype,
        'chartdata': chartdata,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            'donut':True,
            'donutRatio':0.5,
            'chart_attr':{
                'labelType':'\"percent\"',
            }
        }
    }
    return data

def compositionFormatData(data):
    return {'retweet': "{:,}".format(data['retweet']),
            'original': "{:,}".format(data['original']),
            'reply': "{:,}".format(data['reply']),
            } 
    
def compositionPiechartConverter(data):
    """
    pieChart page
    """
    
    xdata = ["Retweet", "Original", "Reply"]
    ydata = [data["retweet"], data["original"], data["reply"]]

    extra_serie = {"tooltip": {"y_start": "", "y_end": ""}}
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype = "pieChart"
    chartcontainer = 'composition_piechart_container'

    data = {
        'chartcontainer': chartcontainer,
        'charttype': charttype,
        'chartdata': chartdata,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            'donut':True,
            'donutRatio':0.5,
            'chart_attr':{
                'labelType':'\"percent\"',
            }
        }
    }
    return data
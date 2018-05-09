# -*- coding: utf-8 -*-
from __future__ import unicode_literals
 
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from .forms import SearchForm
from SMAApp import extract, engagements, wordcloudscript, lda,hashtags
import pandas as pd
import json
import uuid
import os
# Create your views here.

def home(request):
	return get_keyword(request)

def get_keyword(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			print('extracting')
			request.session['user_id'] = str(uuid.uuid4())
			request.session['engagements_data'] = ""
			#df = extract.searchKeyWord(form.cleaned_data['keyword'])
			df = pd.read_pickle("file.pkl")
			request.session["df"] = df
			data = engagements.return_engagements(df)
			formattedData = formatData(data)
			all_data = {}
			all_data["engagements"] = formattedData
			timeline = engagements.return_timeline(df)
			all_data["timeline"] = demo_linechart(request, timeline)
			request.session['engagements_data'] = all_data
			sourceData = engagements.return_source(df)
			sourceFormattedData = sourcePiechartConverter(sourceFormatData(sourceData))
			all_data["source"] = sourceFormattedData
			composition = engagements.return_composition(df)
			compositionFormattedData = compositionPiechartConverter(compositionFormatData(composition))
			all_data["composition"] = compositionFormattedData
			request.session["df"] = df
			return render(request, 'diagnostics.html',
                {'all_data':all_data,'form':form})
	else:
		form = SearchForm()
	return render(request, 'search.html', {'form': form})

def return_geocode(request):
	geoCodes = engagements.return_geocode(request.session["df"])
	return JsonResponse(geoCodes)  

# def return_wordcloud(request):
#     words = wordcloudscript.return_wordcloud(request.session["df"])
#     return JsonResponse(words, safe=False)

def open_diagnostics(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		all_data = request.session['engagements_data']
		form = SearchForm()
		form.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
	return render(request, 'diagnostics.html',
               {'all_data':all_data,'form':form})  
    #template_name = "diagnostics.html"

def open_influencers(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		data = engagements.return_engagements(request.session["df"])
		data['engData'] = engagements.return_influencers(request.session["df"],'engagements')
		data['folData'] = engagements.return_influencers(request.session["df"],'flcount')
		form = SearchForm()
		form.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
	return render(request, 'influencers.html', {'engData':data['engData'],'folData':data['folData'], 'form':form }) 

def open_influentialposts(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		data = engagements.return_infl_posts(request.session["df"])
		form = SearchForm()
		form.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
	return render(request, 'influentialposts.html',{'influentialPost':data, 'form':form})

def open_sentiments(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		chartdata = engagements.return_polarity_chartdata(request.session["df"])
		data = {}
		data['polarityTable'] = engagements.return_polarity(request.session["df"])
		data['polar'] = demo_donutchart(chartdata)
		form = SearchForm()
		form.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
	return render(request, 'sentiments.html', {'sentiments':data,'form':form})

def open_topics(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		chartdata = hashtags.hash_(request.session["df"])
		data = {}
		data["barchart"] = demo_horizontalBarChart(chartdata)
         
		sessionid = request.session["user_id"]
		sessionFilename = "lda-" + sessionid + ".html"
		#path = "C:/Users/christian.dy/Documents/GitHub/SMALab/SMAProject/SMAApp/templates/lda/"
		imageFilename = "wordcloud-" + sessionid + ".png"
		#imagePath = "C:/Users/christian.dy/Documents/GitHub/SMALab/SMAProject/SMAApp/static/images/wordcloud/"
		imagePath = os.path.join(settings.BASE_DIR, "SMAApp\\static\\images\wordcloud\\" + imageFilename)
		ldaPath = os.path.join(settings.BASE_DIR, "SMAApp\\templates\\lda\\" + sessionFilename)
		if not os.path.isfile(ldaPath) or not os.path.isfile(imagePath):
			wordcloudscript.return_wordcloud(request.session["df"], request.session["user_id"])
			lda.lda_model(request.session["df"], request.session["user_id"])
		form = SearchForm()
		form.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
	return render(request, 'topics.html',{'data':data["barchart"], 'sessionid':sessionid,'form':form})

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

def demo_horizontalBarChart(chartdata):
    #nb_element = 10
    xdata = [i["hashtag"] for i in chartdata]
    ydata = [i["count"] for i in chartdata] #[i + random.randint(-10, 10) for i in range(nb_element)]
    #ydata2 = map(lambda x: x * 2, ydata)

    extra_serie = {"tooltip": {"y_start": "", "y_end": " tweets"}}
    kwargs1 = {'color': 'green'}
    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie, **kwargs1
        #'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie,
    }

    charttype = "multiBarHorizontalChart"
    chartcontainer = 'multibarhorizontalchart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
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
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
 
from django.shortcuts import render
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.conf import settings
from .forms import SearchForm
from SMAApp import extract, engagements, wordcloudscript, lda, hashtags, tasks
from SMAApp.models import Snapshot, User
from background_task import background
from django.core import serializers
from celery import shared_task
from celery.result import AsyncResult
from celery.task.control import revoke
import pandas as pd
import json
import uuid
import os
import time
# Create your views here.

tweetCounts = 0

def home(request):
	return get_keyword(request)

def get_keyword(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if 'user_id' in request.session:
			del request.session['user_id']
			del request.session['engagements_data']
			del request.session['df']
		if form.is_valid():
			print("get_keyword")
			print('extracting')
			request.session['user_id'] = str(uuid.uuid4())
			request.session['engagements_data'] = ""
			#df = extract.searchKeyWord(form.cleaned_data['keyword'])[0]
			pickling = os.path.join(settings.BASE_DIR, "SMAApp\\static\\images\\wordcloud\\SM.pkl")
			#df.to_pickle(pickling)
			# df = pd.read_pickle(pickling)
			# request.session["df"] = df

			for snapshotObj in Snapshot.objects(_id='5b3c763c55d14c1cc841393e'):
				print("sash")
				data = snapshotObj.extracted_data
			df = pd.DataFrame(data)
			request.session['df'] = df
				# print(pd.DataFrame(data))
			# Test
			# dict_df = json.loads(df.to_json())
			# diagnostics_data = request.session['engagements_data']
			# # chart_data = Chart()
			request.session['search_keyword'] = form.cleaned_data['keyword']
			# snapshot = Snapshot()
			# snapshot.keyword = form.cleaned_data['keyword']
			# snapshot.platform = 'twitter'
			# # snapshot.snapshot_name = request.GET['name']
			# snapshot.extracted_data = dict_df
			# snapshot.save()
			# print("Heres the id")
			# print(snapshot.pk)

			# user = User()
			# user.snapshots = [snapshot.pk]
			# user.save()
			# Append a Snapshot id reference to User
			# User.objects(id='5b34ed4355d14c2e2c426280').update_one(push__snapshots=snapshot.pk)
			#Test End


			data = engagements.return_engagements(df)
			formattedData = formatData(data)
			quick_stats = {}
			diag_chartdata = {}
			# for key, value in request.session.items(): print('{}'.format(key))
			quick_stats["engagements"] = formattedData
			timeline = engagements.return_timeline(df)
			diag_chartdata["timeline"] = demo_linechart(timeline)
			request.session['timeline_line'] = diag_chartdata["timeline"]
			t1 = time.clock()
			sourceData = engagements.return_source(df)
			t2 = time.clock()
			total = t2 - t1
			print("Source data")
			print(total)
			sourceFormattedData = sourcePiechartConverter(sourceData)
			diag_chartdata["source"] = sourceFormattedData
			t1 = time.clock()
			composition = engagements.return_composition(df)
			t2 = time.clock()
			total = t2 - t1
			print("Composition data")
			print(total)
			compositionFormattedData = compositionPiechartConverter(composition)
			diag_chartdata["composition"] = compositionFormattedData
			request.session['engagements_quick_stats'] = quick_stats
			request.session['engagements_chartdata'] = diag_chartdata
			#Polarity Part
			# request.session["polarity_chartdata"] = engagements.return_polarity_chartdata(df)
			# request.session["polarity_table"] = engagements.return_polarity(df)
			#start_background_tasks(request, df)
			return render(request, 'diagnostics.html',
                {'quick_stats':quick_stats,'diag_chartdata':diag_chartdata,'form':form})
	else:
		form = SearchForm()
	return render(request, 'search.html', {'form': form})

# Returns lat, lang, user, tweet
def return_geocode(request):
	geoCodes = engagements.return_geocode(request.session["df"])
	return JsonResponse(geoCodes)  

def generate_wordcloud_image(request):
	imageFilename = "wordcloud-" + request.session["user_id"] + ".png"
	imagePath = os.path.join(settings.BASE_DIR, "SMAApp\\static\\images\\wordcloud\\" + imageFilename)
	if not os.path.isfile(imagePath):
		print("image not in path")
		wordcloudscript.return_wordcloud(request.session["df"], request.session["user_id"])
		return HttpResponse(False)
	else:
		return HttpResponse(True)

def generate_lda_page(request):
	#sessionFilename = "lda-" + request.session["user_id"] + ".html"
	#ldaPath = os.path.join(settings.BASE_DIR, "SMAApp\\templates\\lda\\" + sessionFilename)	
	#if not os.path.isfile(ldaPath): 
	#if("lda_data" not in request.session and request.session["ldaTriggered"] != 'Y'):
		# print("up")
		# print(request.session["ldaTriggered"])
		# print("nasa if")
		# request.session["ldaTriggered"] = 'Y'
		# print(request.session["ldaTriggered"])
		# lda_data = lda.lda_model(request.session["df"], request.session["user_id"])
		# request.session["lda_data"] = lda_data
		# request.session["ldaTriggered"] = 'N'
		# print(request.session["ldaTriggered"])
	ldapath = os.path.join(settings.BASE_DIR, "SMAApp\\templates\\lda.html")
	html = render_to_string(ldapath)
	return HttpResponse(html)
		# return JsonResponse(request.session["lda_data"],safe=False)
	# else:
	# 	ldapath = os.path.join(settings.BASE_DIR, "SMAApp\\templates\\lda.html")
	# 	html = render_to_string(ldapath, {'ldajson':request.session["lda_data"]})
	# 	return HttpResponse(html)

def test_lda(request):
    df = request.session["df"]
    lda_data = tasks.generate_lda_data.delay(df.to_json())
    request.session["lda_data_id"] = lda_data
    # if request.session.get("lda_data_id",False):
    #     revoke(str(request.session.get('lda_data_id')),terminate=True,signal='SIGKILL')
    #     print("terminated")
    request.session["lda_data"] = lda_data.get()
    for key, value in request.session.items(): print('{}'.format(key))
    request.session.save()
    for key, value in request.session.items(): print('{}'.format(key))
    request.session.modified = True
    # request.session.modified = True
    print("LDA should be settled")
    #return JsonResponse(request.session["lda_data"],safe=False)

def check_lda_status(request):
	# print(request.session.get("lda_data_id",False))
	if request.session.get("lda_data",False):
		return JsonResponse(request.session["lda_data"],safe=False)
	else: 
		return HttpResponse(False)

def save_snapshot(request):
	if request.method == 'POST':
		if request.is_ajax():
			dictio = json.loads(request.POST.get('send_data'))
						# snapshotname = request.POST['snapshotName']
			# insights = request.POST.getlist('insight')
	else:
		return False
	# data_dict = json.JSONDecoder().decode(dictio)
	snapshotName = dictio['snapshotName']
	insights = dictio['insights']
	# chartdata = []
	# diagnostics data
	df = request.session['df']
# # Convert df to dict to save it to db in a Dictfield
	# # dict_df = 
	# # diagnostics_data = request.session['engagements_data']

	# Save chart details
	# chart_data = Chart()
	# chart_data.chart_container = 

	print(df.to_json(orient='records'))
	sasa = df.to_json(orient='records')
	print(sasa)
	# snapshot = Snapshot()
	# snapshot.keyword = request.session['search_keyword']
	# snapshot.platform = 'twitter'
	# snapshot.snapshot_name = snapshotName
	# snapshot.insights = insights
	# snapshot.extracted_data = json.loads(df.to_json(orient='records'))
	# snapshot.date_extracted = df['dateextracted'][0]
	# snapshot.wordcloud_image = 
	# snapshot.save()
	# for snapshotObj in Snapshot.objects(_id='5b3c763c55d14c1cc841393e'):
	# 	print("sash")
	# 	data = snapshotObj.extracted_data
	# 	print(pd.DataFrame(data))
	return True

def start_background_tasks(request):
	df = request.session["df"]
	request.session["sentiments_data_id"] = tasks.generate_sentiments_data.delay(df.to_json())
	request.session["lda_data_id"] = tasks.generate_lda_data.delay(df.to_json())
	request.session.save()

def get_sentiments(request):
	df = request.session["df"]
	print("polarity start")
	t0 = time.clock()
	polarity_chartdata = engagements.return_polarity_chartdata(df)
	t1 = time.clock()
	print("polarity finish")
	total = t1 - t0
	print(total)
	request.session["polarity_chartdata"] = polarity_chartdata 
	polarity_table = engagements.return_polarity(df)
	request.session["polarity_table"] = polarity_table
	# request.session.save()
	request.session.modified = True
	if request.session.get("polarity_chartdata",False) and request.session.get("polarity_table",False):
		return HttpResponse(True)
	else: 
		return HttpResponse(False)
    #request.session["sentiments_chartdata"] = sentiments_data.get()
	

# def return_wordcloud(request):
#     words = wordcloudscript.return_wordcloud(request.session["df"])
#     return JsonResponse(words, safe=False)

def open_diagnostics(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		df = request.session["df"]
		quick_stats = request.session['engagements_quick_stats']
		diag_chartdata = request.session['engagements_chartdata']
		form = SearchForm()
		form.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
	return render(request, 'diagnostics.html',
               {'quick_stats':quick_stats,'diag_chartdata':diag_chartdata,'form':form})

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
		# print(request.session.get('sentiments_data_id', False))
		# sentiments_id = request.session.get('sentiments_data_id', False)
		#sentiments = AsyncResult(str(sentiments_id))
		# Tempo Start
		if not request.session.get("polarity_chartdata",False) or not request.session.get("polarity_table",False):
			polarity_chartdata = engagements.return_polarity_chartdata(request.session["df"])
			request.session["polarity_chartdata"] = polarity_chartdata 
			polarity_table = engagements.return_polarity(request.session["df"])
			request.session["polarity_table"] = polarity_table
		# Tempo End
		# for key, value in request.session.items(): print('{}'.format(key))
		chartdata = request.session.get('polarity_chartdata', False)
		
		#engagements.return_polarity_chartdata(request.session["df"])
		data = {}
		data['polarityTable'] = request.session.get('polarity_table', False)
		#engagements.return_polarity(request.session["df"])
		data['polar'] = demo_donutchart(chartdata)
		form = SearchForm()
		form.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
	return render(request, 'sentiments.html', {'sentiments':data,'form':form})

def open_topics(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		data = {}
		data["barchart"] = hashtags.hash_(request.session["df"])
		
		# data["barchart"] = demo_horizontalBarChart(chartdata)
         
		sessionid = request.session["user_id"]
				#path = "C:/Users/christian.dy/Documents/GitHub/SMALab/SMAProject/SMAApp/templates/lda/"
		#imagePath = "C:/Users/christian.dy/Documents/GitHub/SMALab/SMAProject/SMAApp/static/images/wordcloud/"
		
		# Checks if lda.html or wordcloud image has not yet been been created
		# if not os.path.isfile(imagePath) or not os.path.isfile(ldaPath):
		# 	return HttpResponse(False)
			# wordcloudscript.return_wordcloud(request.session["df"], request.session["user_id"])
			# lda.lda_model(request.session["df"], request.session["user_id"])
		form = SearchForm()
		form.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
	return render(request, 'topics.html',{'tophashtagsdata':data["barchart"], 'sessionid':sessionid,'form':form})

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

def demo_linechart(chartdata):
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
            'jquery_on_ready': False
		}

        
    }

    return data

def demo_donutchart(chartdata):
    """
    pieChart page
    """
    charttype = "pieChart"
    chartcontainer = 'polarity_piechart_container'  # container name
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

def sourcePiechartConverter(chartdata):
    """
    pieChart page
    """
    # {'Web Client': 393, 'Android': 669, 'iPhone': 670, 'Others': 929}
    # xdata = ["Web Client", "Android", "iPhone", "Others"]
    # ydata = [data["webClient"], data["android"], data["iPhone"], data["others"]]
    #ydata = [393, 669, 670, 929]
    #extra_serie = {"tooltip": {"y_start": "", "y_end": ""}}
    #chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
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
    
    chartdata = {
        'x': xdata,
        'name1': 'Tweets', 'y1': ydata, 'extra1': extra_serie
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
			'margin_left' : 120
        }
		
    }
    return data

def compositionFormatData(data):
    return {'retweet': "{:,}".format(data['retweet']),
            'original': "{:,}".format(data['original']),
            'reply': "{:,}".format(data['reply']),
            } 
    
def compositionPiechartConverter(chartdata):
    """
    pieChart page
    """
    
    #xdata = ["Retweet", "Original", "Reply"]
    #ydata = [1307,950,316]
    #ydata = [data["retweet"], data["original"], data["reply"]]

    #extra_serie = {"tooltip": {"y_start": "", "y_end": ""}}
    #chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
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
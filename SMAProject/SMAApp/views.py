# -*- coding: utf-8 -*-
from __future__ import unicode_literals
 
from django.shortcuts import render
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings
from .forms import SearchForm, SnapshotListForm, RegistrationForm
from SMAApp import extract, engagements, wordcloudscript, lda, hashtags, tasks, globals, queries, utils
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
import logging
# Create your views here.

tweetCounts = 0

def home(request):
	return get_keyword(request)

def get_keyword(request):
	if request.method == 'POST':
		searchform = SearchForm(request.POST)
		if 'user_id' in request.session:
			del request.session['user_id']
			del request.session['engagements_data']
			del request.session['df']
		if searchform.is_valid():
			print('extracting')
			request.session['user_id'] = str(uuid.uuid4())
			request.session['engagements_data'] = ""
			#df = extract.searchKeyWord(searchform.cleaned_data['keyword'])[0]
			pickling = os.path.join(settings.BASE_DIR, "SMAApp\\static\\images\\wordcloud\\SM.pkl")
			#df.to_pickle(pickling)
			df = pd.read_pickle(pickling)

			# for snapshotObj in Snapshot.objects(_id='5b3c763c55d14c1cc841393e'):
			# 	data = snapshotObj.extracted_data
			# df = pd.DataFrame(data)
			request.session['df'] = df

			# resultid = tasks.prepareChartData.delay(df.to_json())
			# globals.chartdata['hashtags'] = resultid.get()
			request.session['search_keyword'] = searchform.cleaned_data['keyword']

			# user = User()
			# user.snapshots = [snapshot.pk]
			# user.save()
			# Append a Snapshot id reference to User
			# User.objects(id='5b34ed4355d14c2e2c426280').update_one(push__snapshots=snapshot.pk)

			data = engagements.return_engagements(df)
			formattedData = formatData(data)
			quick_stats = {}
			diag_chartdata = {}

			prepare_chartdata(df)
			# for key, value in request.session.items(): print('{}'.format(key))
			quick_stats["engagements"] = formattedData
			diag_chartdata = create_diag_chartdata()
			# timeline = engagements.return_timeline(df)
			# globals.chartdata["timeline"] = pd.DataFrame(timeline).to_dict(orient='records')
				# diag_chartdata["timeline"] = timeline_linechart(globals.chartdata["timeline"])
				# # sourceData = engagements.return_source(df)
				# sourceFormattedData = sourcePiechartConverter(globals.chartdata["source"])
				# diag_chartdata["source"] = sourceFormattedData
				# # globals.chartdata["source"] = diag_chartdata["source"]
				# compositionFormattedData = compositionPiechartConverter(globals.chartdata["composition"])
				# diag_chartdata["composition"] = compositionFormattedData
			print("Comp Data", globals.chartdata["composition"])
			globals.quick_stats = quick_stats
			globals.diag_chartdata = diag_chartdata
			# globals.chartdata["composition"] = diag_chartdata["composition"]
			request.session['engagements_quick_stats'] = quick_stats
			request.session['engagements_chartdata'] = diag_chartdata
			globals.snapshot_owner = "Dy"
			print("here again")
			globals.SNAPSHOT_LIST = queries.get_snapshot_list()
			# SAVING TEST
			print("INIT")
			# chartdatalist.append(pd.DataFrame(globals.chartdata).to_json(orient='records'))
			# snapshot.wordcloud_image = 
			# snapshot.chart_data = globals.hashtags
			
			# for snapshotObj in Snapshot.objects(owner='Dy'):
			# 	globals.usersnapshotlist.append(snapshotObj.snapshot_name)
			# 	print(globals.usersnapshotlist)

			
			# Set list of snapshots to load snapshots dropdown
			snapshotlistform = SnapshotListForm()
			# CHOICE_GENDER = ((1, 'Male'), (2, 'Female'))
			# globals.snapshotlist = [(snapshotObj.snapshot_name,snapshotObj.snapshot_name) for snapshotObj in Snapshot.objects(owner='Dy')]
			# snapshotform.fields['snapshotchoices'].choices = CHOICE_GENDER #globals.snapshotlist
			isSnapshot = 'false'
			return render(request, 'diagnostics.html',
                {'isSnapshot':isSnapshot,'quick_stats':quick_stats,
				'diag_chartdata':diag_chartdata,
				'searchform':searchform,'snapshotlistform':snapshotlistform})
	else:
		searchform = SearchForm()
	return render(request, 'search.html', {'searchform': searchform})


def open_registration(request):
	if request.method == 'POST':
		print("posted")
		registrationform = RegistrationForm(request.POST)
		if registrationform.is_valid():
			print('Registering')
			isSnapshot = 'false'
			user = User()
			user.username = registrationform.cleaned_data.get('username')
			user.email = registrationform.cleaned_data.get('email')
			user.password = registrationform.cleaned_data.get('password')
			user.address = registrationform.cleaned_data.get('address')
			user.license_type = registrationform.cleaned_data.get('license_type')
			user.save()
			globals.loggedin_userid = user.pk
			print("got search form")
			searchform = SearchForm()
			snapshotlistform = SnapshotListForm()	
			return render(request, 'diagnostics.html',
				{'isSnapshot':isSnapshot,'quick_stats':globals.quick_stats,
				'diag_chartdata':globals.diag_chartdata,'searchform':searchform,
				'snapshotlistform':snapshotlistform})
				# TODO return an else with error message that states form is invalid
		else:
			# if the data has errors, it will default here
			searchform = SearchForm()
			searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
			return render(request, 'registration.html',
			{'searchform':searchform,'registrationform':registrationform})
	else:
		registrationform = RegistrationForm()
		searchform = SearchForm()
		searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
		print("search dapat")
		return render(request, 'registration.html',
		{'searchform':searchform,'registrationform':registrationform})



#  Called after selecting a snapshot from the load snapshot modal
def load_snapshot(request):
	diag_chartdata = {}
	if request.method == 'POST':
		snapshotform = SnapshotListForm(request.POST)
		if snapshotform.is_valid():
			searchform = SearchForm()
			snapshot_id = snapshotform.cleaned_data.get('snapshotchoices')
			# Set values from loaded snapshot
			for snapshotObj in Snapshot.objects(_id=snapshot_id):
				logging.info("Iterating data using snapshot id: %s", snapshot_id)
				request.session['df'] = pd.DataFrame(snapshotObj.extracted_data)
				globals.chartdata['timeline'] = pd.DataFrame(snapshotObj.chart_data[0]['timeline']).to_dict('list')
				globals.chartdata['source'] = pd.DataFrame(snapshotObj.chart_data[0]['source']).to_dict('list')
				globals.chartdata['composition'] = pd.DataFrame(snapshotObj.chart_data[0]['composition']).to_dict('list')
				request.session['engagements_chartdata'] = globals.diag_chartdata
				request.session["lda_data"] = utils.restoreldakeynames(snapshotObj.lda_data)
				print("Printable", pd.DataFrame(snapshotObj.chart_data[0]['composition']).to_dict('list'))
			diag_chartdata = create_diag_chartdata()
			isSnapshot = 'true'
			snapshot_lda_data = request.session["lda_data"]
	# if snapshotlistform.is_valid():
	return render(request, 'diagnostics.html',
            {'isSnapshot':isSnapshot,'quick_stats':globals.quick_stats,
			'diag_chartdata':diag_chartdata,'searchform':searchform,
			'snapshotform':snapshotform,'snapshotLdadata':snapshot_lda_data})

# Sets all data for charts
def prepare_chartdata(df):

    # Data for timeline linechart (Diagnostics Page)
    globals.chartdata["timeline"] = engagements.return_timeline(df)

    # Data for source donut chart (Diagnostics Page)
    globals.chartdata["source"] = engagements.return_source(df)
    

    # Data for composition donut chart (Diagnostics Page)
    globals.chartdata["composition"] = engagements.return_composition(df)

    # Data for hashtags barchart (Topics Page)
    globals.chartdata["hashtags"] = hashtags.hash_(df)

    # Data for polarity donut chart (Sentiments Page)
    globals.chartdata["sentiments"] = engagements.return_polarity_chartdata(df)


# Creates the charts for diagnostics page
def create_diag_chartdata():
	print("Creating Diagnostics chartdata")
	diag_chartdata = {}
	diag_chartdata["timeline"] = timeline_linechart(globals.chartdata["timeline"])
	# sourceData = engagements.return_source(df)
	sourceFormattedData = sourcePiechartConverter(globals.chartdata["source"])
	diag_chartdata["source"] = sourceFormattedData
	# globals.chartdata["source"] = diag_chartdata["source"]
	compositionFormattedData = compositionPiechartConverter(globals.chartdata["composition"])
	diag_chartdata["composition"] = compositionFormattedData
	return diag_chartdata
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
    # TODO redundancy
    globals.lda_data = request.session["lda_data"]
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

# @xframe_options_exempt
def save_snapshot(request):
	print("Saving start")
	if request.method == 'POST':
		if request.is_ajax():
			dictio = json.loads(request.POST.get('send_data'))
						# snapshotname = request.POST['snapshotName']
			# insights = request.POST.getlist('insight')
	else:
		return False
	snapshot_name = dictio['snapshotName']
	insights = dictio['insights']
	chartdatalist = []
	# diagnostics data
	df = request.session['df']
	globals.lda_data = request.session["lda_data"]
	lda_data = utils.removedotsonkey(globals.lda_data) #request.session["lda_data"]

# # Convert df to dict to save it to db in a Dictfield
	# # dict_df = 
	# # diagnostics_data = request.session['engagements_data']

	# Save chart details
	# chart_data = Chart()
	# chart_data.chart_container = 

	print("INIT")
	globals.chartdatafordb["timeline"] = pd.DataFrame(globals.chartdata["timeline"]).to_dict(orient='records')

    # Data for source donut chart (Diagnostics Page)
	globals.chartdatafordb["source"] = pd.DataFrame(globals.chartdata["source"]).to_dict(orient='records')

    # Data for composition donut chart (Diagnostics Page)
	globals.chartdatafordb["composition"] = pd.DataFrame(globals.chartdata['composition']).to_dict(orient='records')

	globals.chartdatafordb["hashtags"] = hashtags.hash_(df)	                            

	# Data for polarity donut chart (Sentiments Page)
	globals.chartdatafordb["sentiments"] = pd.DataFrame(globals.chartdata["sentiments"]).to_dict(orient='records')

	chartdatalist.append(globals.chartdatafordb)
	# chartdatalist.append(globals.chartdata["timeline"])
	# chartdatalist.append(pd.DataFrame(globals.chartdata).to_json(orient='records'))
	# print(chartdatalist)
	snapshot = Snapshot()
	snapshot.keyword = request.session['search_keyword']
	snapshot.platsearchform = 'twitter'
	snapshot.snapshot_name = snapshot_name
	snapshot.insights = insights
	snapshot.extracted_data = json.loads(df.to_json(orient='records'))
	snapshot.date_extracted = df['dateextracted'][0]
	# snapshot.wordcloud_image = 
	snapshot.chart_data = chartdatalist #pd.DataFrame(globals.chartdata).to_json(orient='records') #json.loads(chartdatalist)
	# lda_list = []
	# lda_list.append(lda_data)
	snapshot.lda_data = lda_data
	snapshot.owner = "Dy"
	snapshot.save()

	# Save snapshot id for reference
	snapshotObject = {}
	usersnapshotlist = []
	snapshotObject["value"] = snapshot.pk
	snapshotObject["text"] = snapshot_name
	user = User()
	user.snapshots = [snapshotObject]
	# user.snapshots = [snapshot.pk]
	user.save()
	# Save to list of snapshots if user already logged in
	# if(isLoggedIn):
	User.objects(_id='5b4c58f355d14c1b60591ee6').update_one(push__snapshots=snapshotObject)
	print("SAVED")

	# Get Snapshot list using user id
	# usersnapshotlist = []
	# for userObj in User.objects(_id='5b43845555d14c22b8296ce8'):
	# 	usersnapshotlist = userObj.snapshots
	# 	print("POPO")
	# 	print(usersnapshotlist)

	return HttpResponse("Saved")

def start_background_tasks(request):
	df = request.session["df"]
	request.session["sentiments_data_id"] = tasks.generate_sentiments_data.delay(df.to_json())
	request.session["lda_data_id"] = tasks.generate_lda_data.delay(df.to_json())
	request.session.save()

# Checks if email is already taken
def validate_email(request):
	data = {}
	if request.method == 'GET':
		if request.is_ajax():
			email = request.GET.get('email')
			data = {
				'is_taken': queries.check_if_email_exists(email)
			}
	return JsonResponse(data)
        


def get_sentiments(request):
	df = request.session["df"]
	print("polarity start")
	polarity_chartdata = engagements.return_polarity_chartdata(df)
	print("polarity finish")
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
		searchform = SearchForm()
		searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
		snapshotform = SnapshotListForm()
	return render(request, 'diagnostics.html',
               {'quick_stats':quick_stats,'diag_chartdata':diag_chartdata,'searchform':searchform,'snapshotform':snapshotform})

def open_influencers(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		data = engagements.return_engagements(request.session["df"])
		data['engData'] = engagements.return_influencers(request.session["df"],'engagements')
		data['folData'] = engagements.return_influencers(request.session["df"],'flcount')
		searchform = SearchForm()
		searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
	return render(request, 'influencers.html', {'engData':data['engData'],'folData':data['folData'], 'searchform':searchform }) 

def open_influentialposts(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		data = engagements.return_infl_posts(request.session["df"])
		searchform = SearchForm()
		searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
	return render(request, 'influentialposts.html',{'influentialPost':data, 'searchform':searchform})

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
		chartdata = globals.chartdata["sentiments"] #request.session.get('polarity_chartdata', False)
		
		#engagements.return_polarity_chartdata(request.session["df"])
		data = {}
		data['polarityTable'] = engagements.return_polarity(request.session["df"])
		# data['polarityTable'] = request.session.get('polarity_table', False)
		#engagements.return_polarity(request.session["df"])
		data['polar'] = polarity_donutchart(chartdata)
		searchform = SearchForm()
		searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
	return render(request, 'sentiments.html', {'sentiments':data,'searchform':searchform})

def open_topics(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		data = {}
		data["barchart"] = globals.chartdata["hashtags"]
		# data["barchart"] = demo_horizontalBarChart(chartdata)
         
		sessionid = request.session["user_id"]
				#path = "C:/Users/christian.dy/Documents/GitHub/SMALab/SMAProject/SMAApp/templates/lda/"
		#imagePath = "C:/Users/christian.dy/Documents/GitHub/SMALab/SMAProject/SMAApp/static/images/wordcloud/"
		
		# Checks if lda.html or wordcloud image has not yet been been created
		# if not os.path.isfile(imagePath) or not os.path.isfile(ldaPath):
		# 	return HttpResponse(False)
			# wordcloudscript.return_wordcloud(request.session["df"], request.session["user_id"])
			# lda.lda_model(request.session["df"], request.session["user_id"])
		snapshot_lda_data = request.session["lda_data"]
		searchform = SearchForm()
		searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
	return render(request, 'topics.html',
	{'tophashtagsdata':data["barchart"], 'sessionid':sessionid,
	'searchform':searchform,'snapshotLdadata':json.dumps(snapshot_lda_data)})

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

def timeline_linechart(chartdata):
    """
    lineChart page
    """
    extra_serie = {"tooltip": {"y_start": "", "y_end": "Volume"}}        
    chartdata = {'x': chartdata["xdata"], 'name1': 'Volume', 'y1': chartdata["ydata"], 'kwargs1': { 'color': '#ef6c00' }, 'extra1' : extra_serie}
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

def polarity_donutchart(chartdata):
    """
    pieChart page
    """
    extra_serie = {"tooltip": {"y_start": "", "y_end": ""}}
    chartdata = {'x': chartdata["xdata"], 'y1': chartdata["ydata"], 'name1':'Tweets', 'extra1': extra_serie
    }
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
    extra_serie = {"tooltip": {"y_start": "", "y_end": ""}}
    chartdata = {'x': chartdata["xdata"], 'y1': chartdata["ydata"], 'extra1': extra_serie}
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

    extra_serie = {"tooltip": {"y_start": "", "y_end": ""}}
    chartdata = {'x': chartdata["xdata"], 'y1': chartdata["ydata"], 'extra1': extra_serie}
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
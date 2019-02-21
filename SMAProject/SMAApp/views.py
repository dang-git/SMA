# -*- coding: utf-8 -*-
from __future__ import unicode_literals
 
from django.shortcuts import render
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from mongoengine.queryset import DoesNotExist
from mongoengine import ValidationError
from django.conf import settings
from django.urls import reverse
# from django.contrib.auth.decorators import login_required
from .utils import login_required
from .forms import SearchForm, SnapshotListForm, RegistrationForm, LoginForm
from .chartdata import ChartData
from SMAApp import extract, engagements, wordcloudscript, lda, hashtags, tasks, globals, queries, utils, chartcreator
from SMAApp import smaapp_constants as constants
from SMAApp.models import Snapshot, User, Names, WordCloudImageMask
from background_task import background
from django.core import serializers
from celery import shared_task, task
from celery.result import AsyncResult
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage

# from celery.task.control import revoke
import pandas as pd
import json
import uuid
import os
import time
import logging
import bcrypt
import numpy as np
import sys
from bson import errors
# Create your views here.

def home(request):
	if 'isloggedin' in request.session:
		return get_keyword(request)
	else:
		return login_user(request)

def get_keyword(request):
	if request.method == 'POST':
		searchform = SearchForm(request.POST)
		if 'user_id' in request.session:
			del request.session['user_id']
			del request.session['engagements_data']
			del request.session['df']
		if searchform.is_valid():
			print('extracting')
			# utils.clear_specific_sessionkeys(request)
			if request.session.get("lda_data",False):
				del request.session['lda_data']
			request.session['user_id'] = request.session.session_key #str(uuid.uuid4())
			request.session['engagements_data'] = ""
			df = extract.searchKeyWord(searchform.cleaned_data['keyword'])[0]
			#pickling = os.path.join(settings.BASE_DIR, "SMAApp\\pkls\\SM.pkl")
			#df.to_pickle(pickling)
			#df = pd.read_pickle(pickling)

			#df = pd.DataFrame(data)
			request.session['df'] = df
			request.session['search_keyword'] = searchform.cleaned_data['keyword']

			# user = User()
			# user.snapshots = [snapshot.pk]
			# user.save()
			# Append a Snapshot id reference to User
			# User.objects(id='5b34ed4355d14c2e2c426280').update_one(push__snapshots=snapshot.pk)
			quick_stats = {}
			quick_stats_data = engagements.return_engagements(df)
			request.session['quick_stats_db'] = quick_stats_data
			quick_stats = format_quick_stats_comma(quick_stats_data)
			request.session["quick_stats"] = quick_stats
			diag_chartdata = {}
			request.session['chartdata'] = prepare_chartdata(df)
			diag_chartdata = create_diag_chartdata(request.session['chartdata'])

			request.session["diag_chartdata"] = diag_chartdata

			# Prepare data for influencers and influential posts
			request.session["influencers_data"] = prepare_influencers_data(df)
			request.session["influential_data"] = prepare_influentialposts_data(df)
			
			snapshotlistform = SnapshotListForm(request=request)
			loginform = LoginForm()

			request.session['isSnapshot'] = 'false'

			# Generate Wordcloud image (PIL image type)
			request.session['pil_image_str'] = generate_wordcloud_image(request)
			# Base64 form of image (Binary)
			request.session['wc_image_str'] = utils.convert_to_base64(request.session['pil_image_str'])
			username = ""
			if request.session.get('loggedin_username'):
				username = request.session['loggedin_username']
			return render(request, 'diagnostics.html',
                {'isSnapshot':request.session['isSnapshot'],'quick_stats':quick_stats,
				'diag_chartdata':diag_chartdata,
				'searchform':searchform,'snapshotlistform':snapshotlistform,
				'loginform':loginform,'username':username})
	else:
		if 'isloggedin' in request.session and 'search_keyword' in request.session:
			return HttpResponseRedirect(reverse('diagnostics'))
		else:
			searchform = SearchForm()
	return render(request, 'search.html', {'searchform': searchform})

# Sets all data for charts
def prepare_chartdata(df):
	chartdata = ChartData()
    # Data for timeline linechart (Diagnostics Page)
	chartdata.timeline = engagements.return_timeline(df)

    # Data for source donut chart (Diagnostics Page)
	chartdata.source =  engagements.return_source(df)

    # Data for composition donut chart (Diagnostics Page)
	chartdata.composition = engagements.return_composition(df)

    # Data for hashtags barchart (Topics Page)
	chartdata.hashtags = hashtags.hash_(df)

    # Data for polarity donut chart (Sentiments Page)
	chartdata.sentiments = engagements.return_polarity_chartdata(df)
	chartdata.polarity_table = engagements.return_polarity(df)

	return chartdata

def login_user(request):
	if request.method == 'POST':
		loginform = LoginForm(request.POST)
		if loginform.is_valid():
			email =  loginform.cleaned_data.get('email')
			password = loginform.cleaned_data.get('password')
			# user1 = authenticate(email=email,password=password)
			try:
				user = User.objects.get(email=email)
			except DoesNotExist:
				messages.error(request, constants.USER_DOES_NOT_EXIST)
				return render(request, 'loginpage.html', {'loginform': loginform})
			if bcrypt.checkpw(password.encode('utf8'),user.password.encode('utf8')):
				# TODO redundancy
				# for key, value in request.session.items(): print('{}'.format(key))
				request.session['loggedin_userid'] = user.id
				request.session['loggedin_username'] = user.username
				request.session['isSnapshot'] = 'false'
				request.session['isloggedin'] = True
				searchform = SearchForm()
				authenticated = 'True'
				messages.success(request, constants.LOGIN_SUCCESS)
				request.session['snapshot_list'] = queries.get_snapshot_list(user.id)
				return render(request, 'search.html', {'searchform': searchform})
			else:
				authenticated = 'False'
				messages.error(request, 'Wrong credentials')
				return render(request, 'loginpage.html', {'loginform': loginform})
	else:
		if 'isloggedin' in request.session:
			searchform = SearchForm()
			return render(request, 'search.html', {'searchform': searchform})
		else:
			loginform = LoginForm()
	return render(request, 'loginpage.html', {'loginform': loginform})


def ajax_login_user(request):
	authenticated = 'False'
	if request.method == 'POST':
		if request.is_ajax():
			try:
				user_credentials = json.loads(request.POST.get('user_credentials'))
				user = User.objects.get(email=user_credentials['email'])
				# print("usercontents", dict(user.to_mongo()))
				if bcrypt.checkpw(user_credentials['password'].encode('utf8'),user.password.encode('utf8')):
					# TODO redundancy
					# for key, value in request.session.items(): print('{}'.format(key))
					request.session['loggedin_userid'] = user.id
					request.session['loggedin_username'] = user.username
					request.session['isSnapshot'] = 'false'
					request.session['isloggedin'] = True
					# searchform = SearchForm()
					# snapshotlistform = SnapshotListForm()
					authenticated = 'True'
					messages.success(request, constants.LOGIN_SUCCESS)
					# return HttpResponseRedirect(reverse('diagnostics'))
					request.session['snapshot_list'] = queries.get_snapshot_list(user.id)
					return JsonResponse(authenticated, status=200, safe=False)
				else:
					authenticated = 'False'
					# messages.error(request, 'Wrong credentials')
					# json = json.dumps({'authenticated': False})
					return JsonResponse(authenticated, status=401, safe=False)
			except User.DoesNotExist:
				authenticated = 'False'
				return JsonResponse(authenticated, status=401, safe=False)	
	return JsonResponse(authenticated, status=401, safe=False)
				# return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	# Compares the user entered password to hashed password from db
	# if bcrypt.checkpw(request.POST['password'].encode('utf8'),user.password.encode('utf8')):
	# 	print("success")	
	# else:
	# 	print("unsuccess")
	# 	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	# 	if user.check_password(request.POST['password']):
	# 		user.backend = 'mongoengine.django.auth.MongoEngineBackend'
	# 		login(request, user)
	# 		request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
	# 		return HttpResponse(user)
	# 	else:
	# 		return HttpResponse('login failed')
	# except DoesNotExist:
	# 	return HttpResponse('user does not exist')
	# except Exception:
	# 	return HttpResponse('unknown error')

def logout_user(request):
	# request.session.flush()
	logout(request)
	return HttpResponseRedirect("/")

def open_registration(request):
	loginform = LoginForm()
	registrationform = RegistrationForm()
	searchform = SearchForm()
	if request.session.get('isloggedin'):
		return HttpResponseRedirect(reverse('diagnostics'))
	else:
		if request.method == 'POST':
			registrationform = RegistrationForm(request.POST)
			if registrationform.is_valid():
				print('Registering')
				request.session['isSnapshot'] = 'false'
				user = User()
				user.username = registrationform.cleaned_data.get('username')
				user.email = registrationform.cleaned_data.get('email')
				# Hash password before inserting it into db
				password = registrationform.cleaned_data.get('password')
				salt = bcrypt.gensalt(constants.SALT_WORK_FACTOR)
				hashed_password = bcrypt.hashpw(password.encode('utf8'),salt)
				user.password = hashed_password.decode("utf8")
				user.address = registrationform.cleaned_data.get('address')
				user.license_type = registrationform.cleaned_data.get('license_type')
				user.save()
				request.session['loggedin_userid'] = user.pk
				request.session['loggedin_username'] = user.username

				# Create a snapshot_list key so we won't get KeyError
				request.session['snapshot_list'] = []
				return HttpResponseRedirect(reverse('diagnostics'))
				# return render(request, 'diagnostics.html',
				# 	{'isSnapshot':isSnapshot,'quick_stats':globals.quick_stats,
				# 	'diag_chartdata':globals.diag_chartdata,'searchform':searchform,
				# 	'snapshotlistform':snapshotlistform})
					# TODO return an else with error message that states form is invalid
			else:
				# if the data has errors, it will default here
				searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
				return render(request, 'registration.html',
				{'searchform':searchform,'registrationform':registrationform,'loginform':loginform})
		else:
			searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
			return render(request, 'registration.html',
			{'searchform':searchform,'registrationform':registrationform, 'loginform':loginform})

def get_snapshot_lda(request):
	if "lda_data" in request.session and request.session["isSnapshot"] == 'true':
		return JsonResponse(request.session["lda_data"],safe=False)
	else: 
		return HttpResponse(False)

#  Called after selecting a snapshot from the load snapshot modal
def load_snapshot(request):
	diag_chartdata = {}
	request.session['isSnapshot'] = 'true'
	isSnapshot = 'true'
	searchform = SearchForm()
	snapshot_lda_data = {}
	insight = {}
	insights_fromdb = []
	username = get_username(request)
	if request.method == 'POST':
		snapshotlistform = SnapshotListForm(request.POST)
		print("snap errors", snapshotlistform.errors)
		if snapshotlistform.is_valid():
			snapshot_id = request.POST.get('snapshotchoices')
			if snapshot_id is not None:
				# snapshot_id = snapshotlistform.cleaned_data['snapshotchoices']
				# Set values from loaded snapshot
				for snapshot_obj in Snapshot.objects(_id=snapshot_id):
					logging.info("Iterating data using snapshot id: %s", snapshot_id)
					request.session['search_keyword'] = snapshot_obj.keyword
					request.session['df'] = pd.DataFrame(snapshot_obj.extracted_data)
					# chartdata = {}
					chartdata = ChartData()
					chartdata.timeline = pd.DataFrame(snapshot_obj.chart_data[0]['timeline']).to_dict('list')
					chartdata.source = pd.DataFrame(snapshot_obj.chart_data[0]['source']).to_dict('list')
					chartdata.composition = pd.DataFrame(snapshot_obj.chart_data[0]['composition']).to_dict('list')
					chartdata.hashtags = snapshot_obj.chart_data[0]['hashtags']
					chartdata.sentiments = pd.DataFrame(snapshot_obj.chart_data[0]['sentiments']).to_dict('list')
					chartdata.polarity_table = snapshot_obj.chart_data[0]['polarity_table'][0] # Access the dict inside the list thats why theres another [0] after the polarity table
					# chartdata['timeline'] = pd.DataFrame(snapshot_obj.chart_data[0]['timeline']).to_dict('list')
					# chartdata['source'] = pd.DataFrame(snapshot_obj.chart_data[0]['source']).to_dict('list')
					# chartdata['composition'] = pd.DataFrame(snapshot_obj.chart_data[0]['composition']).to_dict('list')
					# chartdata['hashtags'] = snapshot_obj.chart_data[0]['hashtags']
					# chartdata['sentiments'] = pd.DataFrame(snapshot_obj.chart_data[0]['sentiments']).to_dict('list')
					# chartdata['polarity_table'] = snapshot_obj.chart_data[0]['polarity_table'][0] # Access the dict inside the list thats why theres another [0] after the polarity table
					request.session['chartdata'] = chartdata
					diag_chartdata = create_diag_chartdata(chartdata)
					request.session['diag_chartdata'] = diag_chartdata

					# Returns a list of insights
					insights_fromdb = snapshot_obj.insights
					# Extract insights from list of insights
					if insights_fromdb is not None:
						for idx, insights in enumerate(insights_fromdb):
							insight[idx] = insights

					# wc_image = snapshot_obj.wordcloud_image.read()
					# wc_image_content_type = snapshot_obj.wordcloud_image.content_type
					quick_stats_data = snapshot_obj.quick_stats
					request.session['quick_stats_db'] = quick_stats_data
					request.session['influencers_data'] = snapshot_obj.influencers_data
					request.session['influential_data'] = snapshot_obj.influential_data
					request.session['quick_stats'] = format_quick_stats_comma(quick_stats_data)
					
					# PIL Image way 
					# print("snapshot_obj.wordcloud_image", snapshot_obj.wordcloud_image.width)
					request.session['wc_image_str'] = utils.convert_to_base64(snapshot_obj.wordcloud_image.read())
					# request.session['wc_image_str'] = utils.convert_to_base64(snapshot_obj.wordcloud_image)
					# Base64 way
					# request.session['wc_image_str'] = snapshot_obj.wordcloud_image
					snapshot_lda_data = utils.restore_lda_keynames(snapshot_obj.lda_data)
					request.session["lda_data"] = snapshot_lda_data
				
				# snapshotlistform = SnapshotListForm(initial={'max_number': '3'})
				request.session['selected_snapshot'] = snapshot_id
				request.session['current_snapshot'] = snapshot_id
				snapshotlistform = SnapshotListForm(request=request)
				# snapshotListFormInstance.fields['snapshotchoices'].initial = [snapshot_id]
				messages.success(request,constants.LOADING_SNAPSHOT_SUCCESS)
			else:
				messages.error(request,"Blank snapshot not loaded.")
				return HttpResponseRedirect(reverse('diagnostics'))
		else:
			return render(request, 'diagnostics.html',
			{'isSnapshot':isSnapshot,'quick_stats':request.session['quick_stats'],
			'diag_chartdata':diag_chartdata,'searchform':searchform,
			'snapshotlistform':snapshotlistform,'insight':insight,'username':username,
			'search_keyword':request.session['search_keyword']})
	else:
		return HttpResponseRedirect(reverse('diagnostics'))
	return render(request, 'diagnostics.html',
            {'isSnapshot':isSnapshot,'quick_stats':request.session['quick_stats'],
			'diag_chartdata':diag_chartdata,'searchform':searchform,
			'snapshotlistform':snapshotlistform,'insight':insight,
			'username':username,'search_keyword':request.session['search_keyword'],
			'wc_image':request.session['wc_image_str']})

def prepare_influencers_data(df):
	data = {}
	data['engData'] = engagements.return_influencers(df,'engagements')
	data['folData'] = engagements.return_influencers(df,'flcount')
	return data

def prepare_influentialposts_data(df):
	data = {}
	data = engagements.return_infl_posts(df)
	return data

# Creates the charts for diagnostics page
def create_diag_chartdata(chartdata):
	print("Creating Diagnostics chartdata")
	# diag_chartdata = {}
	diag_chartdata = ChartData()
	diag_chartdata.timeline = chartcreator.timeline_linechart(chartdata.timeline)
	diag_chartdata.source = chartcreator.sourcePiechartConverter(chartdata.source)
	diag_chartdata.composition = chartcreator.compositionPiechartConverter(chartdata.composition)
	# diag_chartdata["timeline"] = chartcreator.timeline_linechart(chartdata.timeline)
	# diag_chartdata["source"] = chartcreator.sourcePiechartConverter(chartdata.source)
	# diag_chartdata["composition"] = compositionPiechartConverter(chartdata.composition)
	return diag_chartdata

# Returns lat, lang, user, tweet
def return_geocode(request):
	geoCodes = engagements.return_geocode(request.session["df"])
	return JsonResponse(geoCodes)  

def generate_wordcloud_image(request):
	# image_filename = "wordcloud-" + request.session["user_id"] + ".png"
	# image_path = os.path.join(settings.BASE_DIR, "SMAApp\\static\\images\\wordcloud\\" + image_filename)
	# if request.session['isSnapshot'] != 'true':
		# if not os.path.isfile(image_path):
	print("Creating img")
	wcmask_url = None
	if 'wcmask_url' in request.session:
		wcmask_url = request.session['wcmask_url']
	pil_img_str = wordcloudscript.return_wordcloud(wcmask_url, request.session["df"])
	print("img is created")
	return pil_img_str #HttpResponse(img_str)
		# else:
		# 	return HttpResponse(True)
	# else:
		# return HttpResponse(request.session['wc_image_str'])
		# wc_image = request.session['wc_image']
		# wc_image_content_type = request.session['wc_image_content_type']
		# return HttpResponse(wc_image, mimetype=wc_image_content_type)
def generate_lda_page(request):
	#sessionFilename = "lda-" + request.session["user_id"] + ".html"
	#ldaPath = os.path.join(settings.BASE_DIR, "SMAApp\\templates\\lda\\" + sessionFilename)	
	#if not os.path.isfile(ldaPath): 
	#if("lda_data" not in request.session and request.session["ldaTriggered"] != 'Y'):
		# print(request.session["ldaTriggered"])
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

def start_generate_lda(request):
	# if request.method == 'POST':
	# 	if request.is_ajax():
	# 		num_topics = request.POST.get('num_topics')
	df = request.session["df"]
	num_topics = 4
	lda_task_id = tasks.generate_lda_data.delay(num_topics, df.to_json())
	request.session["lda_task_id"] = lda_task_id
    # if request.session.get("lda_data_id",False):
    #     revoke(str(request.session.get('lda_data_id')),terminate=True,signal='SIGKILL')
    #     print("terminated")
    # request.session["lda_data"] = lda_task_id.get()
    # for key, value in request.session.items(): print('{}'.format(key))
    # request.session.modified = True
	return HttpResponse(True)

def check_lda_status(request):
	if "lda_task_id" in request.session and "lda_data" not in request.session:
		lda_task_id = request.session['lda_task_id']
		print('lda_task_id is present')
		if lda_task_id.ready():
			request.session["lda_data"] = lda_task_id.get()
			print("LDA data is ready and sent")
	if request.session.get("lda_data",False):
		print("there is lda data")
		return JsonResponse(request.session["lda_data"],safe=False)
	else: 
		return HttpResponse(False)

def save_snapshot(request):
	if request.method == 'POST':
		if request.is_ajax():
			snapshot_ajax_data = json.loads(request.POST.get('send_data'))
						# snapshotname = request.POST['snapshotName']
			# insights = request.POST.getlist('insight')
			snapshot_name = snapshot_ajax_data['snapshotName']
			insights = snapshot_ajax_data['insights']

			if 'current_snapshot' in request.session:
				updated = Snapshot.objects.filter(id=request.session['current_snapshot']).update(insights=insights)
				if updated == 1:
					messages.success(request, constants.INSIGHTS_UPDATE_SUCCESS)
					return HttpResponse(status=200)
			else:
				chartdatalist = []
				
				# diagnostics data
				df = request.session['df']
				lda_data = request.session["lda_data"]
				lda_data = utils.remove_dots_on_key(lda_data) #request.session["lda_data"]

				# # Convert df to dict to save it to db in a Dictfield
				# # dict_df = 
				# # diagnostics_data = request.session['engagements_data']

				# chartdata = {}
				chartdata = ChartData()
				chartdata = request.session['chartdata']
				chartdatafordb = {}
				chartdatafordb["timeline"] = pd.DataFrame(chartdata.timeline).to_dict(orient='records')

				# Data for source donut chart (Diagnostics Page)
				chartdatafordb['source'] = pd.DataFrame(chartdata.source).to_dict(orient='records')

				# Data for composition donut chart (Diagnostics Page)
				chartdatafordb['composition'] = pd.DataFrame(chartdata.composition).to_dict(orient='records')

				chartdatafordb['hashtags'] = chartdata.hashtags

				# Data for polarity donut chart (Sentiments Page)
				chartdatafordb['sentiments'] = pd.DataFrame(chartdata.sentiments).to_dict(orient='records')

				# Set Polarity into a list so it can be saved as an array
				polarity_table_holder = []
				polarity_table_holder.append(chartdata.polarity_table)
				chartdatafordb['polarity_table'] = polarity_table_holder
				chartdatalist.append(chartdatafordb)

				# for key, value in request.session.items(): print('{}'.format(key))
				snapshot = Snapshot()
				snapshot.keyword = request.session['search_keyword']
				snapshot.platform = 'twitter'
				snapshot.snapshot_name = snapshot_name
				snapshot.insights = insights
				snapshot.extracted_data = json.loads(df.to_json(orient='records'))
				snapshot.quick_stats = request.session['quick_stats_db']
				snapshot.influencers_data = request.session['influencers_data']
				snapshot.influential_data = request.session['influential_data']
				snapshot.date_extracted = df['dateextracted'][0]

				# Temporary Image way
				# Get image as temp
				tempImg_obj = utils.create_temp_img_file(request.session['pil_image_str'])
				snapshot.wordcloud_image.put(tempImg_obj, content_type='image/png')

				# Save wc_image as binary. ex: b'iVBOR.....' with the b' infront
				# snapshot.wordcloud_image = request.session['wc_image_str']
				snapshot.chart_data = chartdatalist #pd.DataFrame(globals.chartdata).to_json(orient='records') #json.loads(chartdatalist)
				# lda_list = []
				# lda_list.append(lda_data)
				snapshot.lda_data = lda_data
				snapshot.owner = request.session['loggedin_userid']
				try:
					snapshot.save()
				except ValidationError as e:
					messages.error(request,constants.SAVING_ERROR)
					return HttpResponse(status=403)

				# snapshot.reload()
				print("Snapshot successfully saved")
				snapshotObject = {}
				if snapshot.pk is not None:
					request.session['current_snapshot'] = snapshot.id
					# Save snapshot id for reference
					snapshotObject["value"] = snapshot.pk
					snapshotObject["text"] = snapshot_name
					User.objects(_id=request.session['loggedin_userid']).update_one(push__snapshots=snapshotObject)
					print("Snapshot saved in user object")
					# user = User()
					# user.snapshots = [snapshotObject]
					# user.save()
					# user.snapshots = [snapshot.pk]
						
					# Update dropdown's snapshot list
					# if request.session.get('snapshot_list',[]):
					snapshot_list = request.session['snapshot_list']
					snapshot_list.append((snapshotObject['value'],snapshotObject['text']))
					request.session['snapshot_list'] = snapshot_list
					snapshotListForm = SnapshotListForm(request=request)
					snapshotListForm.fields['snapshotchoices'].choices = request.session['snapshot_list'] #queries.get_snapshot_list(request.session['loggedin_userid'])
					messages.success(request,constants.SAVING_SUCCESS)
					return HttpResponse(status=200)
		else:
			messages.error(request,constants.SAVING_ERROR)
			return HttpResponse(status=401)
	
	# return HttpResponseRedirect(reverse('diagnostics'))
	# return render(request, 'diagnostics.html',
    #            {'quick_stats':quick_stats,
	# 		   'diag_chartdata':diag_chartdata,
	# 		   'searchform':searchform,
	# 		   'snapshotlistform':snapshotlistform,
	# 		   'loginform':loginform,
	# 		   'username':globals.loggedin_username})

# Checks if email is already taken
def validate_registration_email(request):
	data = {}
	if request.method == 'GET':
		if request.is_ajax():
			email = request.GET.get('email')
			data = {
				'is_taken': queries.check_if_email_exists(email)
			}
	return JsonResponse(data)

# def return_wordcloud(request):
#     words = wordcloudscript.return_wordcloud(request.session["df"])
#     return JsonResponse(words, safe=False)

def get_username(request):
	username = ""
	if request.session.get("loggedin_username",False):
		username = request.session['loggedin_username']
	return username

@login_required
def open_diagnostics(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		quick_stats = request.session['quick_stats']
		diag_chartdata = request.session['diag_chartdata']
		searchform = SearchForm()
		searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
		snapshotlistform = SnapshotListForm(request=request)
		loginform = LoginForm()
		username = get_username(request)
	return render(request, 'diagnostics.html',
               {'quick_stats':quick_stats,
			   'diag_chartdata':diag_chartdata,
			   'searchform':searchform,
			   'snapshotlistform':snapshotlistform,
			   'loginform':loginform,
			   'username':username})

@login_required
def open_influencers(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		data = {}
		data['engData'] = request.session['influencers_data']['engData']
		data['folData'] = request.session['influencers_data']['folData']
		searchform = SearchForm()
		searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
		snapshotlistform = SnapshotListForm(request=request)
		loginform = LoginForm()
		username = get_username(request)
	return render(request, 'influencers.html',
	 {'engData':data['engData'],'folData':data['folData'],
	  'searchform':searchform,'snapshotlistform':snapshotlistform,
	   'loginform':loginform,'username':username}) 

@login_required
def open_influentialposts(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		data = request.session['influential_data']
		searchform = SearchForm()
		searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
		snapshotlistform = SnapshotListForm(request=request)
		loginform = LoginForm()
		username = get_username(request)
	return render(request, 'influentialposts.html',
	{'influentialPost':data, 'searchform':searchform,
	'snapshotlistform':snapshotlistform,'loginform':loginform,'username':username})

@login_required
def open_sentiments(request):
	if request.method == 'POST':
		get_keyword(request)
	else:
		data = {}
		chartdata = request.session['chartdata']
		# data['polarityTable'] = request.session['chartdata']['polarity_table']
		data['polarityTable'] = chartdata.polarity_table
		data['polar'] = chartcreator.polarity_donutchart(chartdata.sentiments)
		searchform = SearchForm()
		searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
		snapshotlistform = SnapshotListForm(request=request)
		loginform = LoginForm()
		username = get_username(request)
	return render(request, 'sentiments.html', 
	{'sentiments':data,'searchform':searchform,
	'snapshotlistform':snapshotlistform,'loginform':loginform,'username':username})

@login_required
def open_topics(request):
	# if request.method == 'POST' and 'uploadwcMaskButton' in request.POST:
	# 	upload_wordcloud_mask(request)
	if request.method == 'POST':
		get_keyword(request)
	else:
		data = {}
		# data["barchart"] = request.session["chartdata"]["hashtags"]
		chartdata = request.session['chartdata']
		data["barchart"] = chartdata.hashtags
		# data["barchart"] = chartcreator.hashtag_horizontalBarChart(chartdata)
         
		sessionid = request.session["user_id"]
		
		# Checks if lda.html or wordcloud image has not yet been been created
		# if not os.path.isfile(imagePath) or not os.path.isfile(ldaPath):
		# 	return HttpResponse(False)
			# wordcloudscript.return_wordcloud(request.session["df"], request.session["user_id"])
			# lda.lda_model(request.session["df"], request.session["user_id"])
			
		# snapshot_lda_data = request.session["lda_data"]
		# 'snapshotLdadata':json.dumps(snapshot_lda_data)
		searchform = SearchForm()
		searchform.fields['keyword'].widget.attrs['placeholder'] = "Search #hashtag"
		snapshotlistform = SnapshotListForm(request=request)
		loginform = LoginForm()
		username = get_username(request)
	return render(request, 'topics.html',
	{'tophashtagsdata':data["barchart"], 'sessionid':sessionid,
	'searchform':searchform,'snapshotlistform':snapshotlistform,
	'loginform':loginform,'username':username,'wc_image':request.session['wc_image_str'].decode('utf-8')})

# FileSystemStorage already appends a string to the uploaded filename
# so that it won't be overwritten if another file with the same filename has been uploaded
def upload_wordcloud_mask(request):
	if request.is_ajax():
		if request.method == 'POST': # and request.FILES['wc_mask']:
			wc_mask = request.FILES['wc_mask']
			fs = FileSystemStorage()
			filename = fs.save(wc_mask.name,wc_mask)
			uploaded_file_url = fs.url(filename)
			request.session['wcmask_url'] = uploaded_file_url
			#  Recreate image and set it to session.
			request.session['pil_image_str'] = generate_wordcloud_image(request)
			request.session['wc_image_str'] = utils.convert_to_base64(request.session['pil_image_str'])
			path = settings.MEDIA_ROOT + "\\" + filename
			# Remove uploaded photo from media folder after being converted into base64 image
			os.remove(path)
			return HttpResponse(request.session['wc_image_str'])

def format_quick_stats_comma(data):
 	return	{'users': "{:,}".format(data['users']),
                  'tweets': "{:,}".format(data['tweets']),
                  'engagements': "{:,}".format(data['engagements']),
                  'reach': "{:,}".format(data['reach'])}
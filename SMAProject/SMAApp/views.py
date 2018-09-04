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
from SMAApp import extract, engagements, wordcloudscript, lda, hashtags, tasks, globals, queries, utils
from SMAApp import smaapp_constants as constants
from SMAApp.models import Snapshot, User, Names
from background_task import background
from django.core import serializers
from celery import shared_task, task
from celery.result import AsyncResult
from django.contrib.auth import authenticate

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

def insert_names():
	names = ['camacho', 'jason', 'ron', 'alcantara-banaybanay', 'rob', 'cynthia', 'sonja', 'roy', 'gahon', 'mejia', 'rosales', 'tuba', 'maquilan', 'galvez', 'abdurahman', 'jerome', 'jessie', 'rutor', 'pedro', 'keith', 'sabalburo', 'marissa', 'santosghel', 'april', 'anjannette', 'riza', 'salido', 'rg', 'tj', 'balderama', 'estanislao', 'oliveros', 'tvpatrol', 'scarlett', 'icasiano-ruiz', 'dela', 'secondez,ly', 'labong', 'ayyie', 'augusto', 'hannah', 'aurora', 'gerodias', 'evardome', 'jacq', 'vera', 'bugna', 'lhenyet', 'sol', 'besinal', 'ivanong', 'hya', 'joed', 'ofrin', 'erlinda', 'esperanza', 'dumaguing', 'philippines', 'solatorio', 'michael', 'dia', 'ryan', 'ri', 'p', 'harry', 'elah', 'venus', 'caryl', 'orzo', 'louie', 'zabarte', 'inot', 'zhav', 'tel', 'osinsao', 'musñgi', 'teo', 'jerelyn', 'abarquez', 'falcis', 'jc', 'galay', 'mangaliman', 'marilyn', 'arnold', 'rodmar', 'elise', 'redrose', 'belleza', 'capalad', 'rosauro', 'celestino', 'jochelle', 'cely', 'vitorillo', 'kris', 'canales', 'barrientos', 'lising', 'laurence', 'haze', 'binabay', 't', 'joycie', 'net', 'roann', 'jayson', 'phoebe', 'christian', 'dahl', 'laborre', 'therese', 'henry', 'jasmine', 'avigail', 'leo', 'ching', 'simon', 'janessa', 'jhunski', 'josol', 'odero', 'pacis', 'relly', 'terrence', 'bemon', 'calter', 'marionne', 'heracleo', 'louise', 'nodalo', 'alyssa', 'raffytulfo', 'aki', 'ramos', 'lizette', 'cindy', 'dasco', 'cathy', 'janice', 'rlndblnsg', 'dre', 'agustin', 'jann', 'robillos', 'sirc', 'mendozadel', 'apple', 'apyang', 'julie', 'boqx', 'bro', 'rhonn', 'austria', 'alinsod', 'aimee', 'kristina', 'elizaga', 'baltazar', 'gagalang', 'ishibashi', 'trinidad', 'angelo', 'cha', 'tels', 'jayme', 'andaya', 'barrios', 'mendoza', 'nava', 'charie', 'aya', 'ambid', 'elleyn', 'rodriguez', 'salash', 'presquito', 'bonilla', 'chu', 'galguerra', 'morc', 'jonathan', 'seguerra', 'baba', 'escalona', 'miayo', 'sarmiento', 'baliuag', 'aiza', 'israel', 'yvaine', 'casey', 'barcellano', 'dios', 'tesalona', 'zamora', 'chastine', 'secuya', 'conje', 'esquivel', 'te', 'ma', 'caguiat', 'rayson', 'gabriel', 'mo', 'krizza', 'albon', 'jude', 'mj', 'nina', 'arches', 'archer', 'del', 'era', 'flo', 'julliane', 'bojo', 'ernest', 'olivar', 'dee', 'zafe', 'heart', 'gerly', 'rappler', 'shara', 'milagrosa', 'amalia', 'dato-on', 'honey', 'naome', 'allauigan', 'daiserie', 'malig-on', 'nobleza', 'tan', 'agena', 'angielyn', 'sis', 'mendoza-del', 'reyespia', 'silos', 'russelloto', 'roderos', 'lorisse', 'cabrillos', 'ava', 'camille', 'brian', 'sia', 'mayores', 'gallart', 'mari', 'reyes', 'enz', 'fortaliza', 'divo', 'masujer', 'mar', 'dadia', 'elizabeth', 'gmanews', 'ayala', 'may', 'alojado', 'hong', 'alegre', 'ronald', 'levi', 'margret', 'actiontv', 'rosanna', 'mai', 'alindada', 'avengers', 'malena', 'a', 'abe', 'beltran', 'azzupary', 'pamparo-castrillo', 'rosalinda', 'arciento', 'q', 'umagang', 'claire', 'riezel', 'martina', 'pangilinan-po', 'gerard', 'buge', 'paz', 'castillejos',
         'sd', 'shiela', 'voluntarioso', 'navarroanj', 'johnell', 'josephine', 'quiño', 'orana', 'yvonne', 'emmanuel', 'caudilla', 'modesto', 'mabel', 'dagaraga', 'mallari', 'glen', 'jian', 'josie', 'runas', 'zepeda', 'amaloveina', 'yucai', 'lu', 'dolly', 'romarico', 'santelices', 'taylo', 'esem', 'rara', 'jady', 'balungcas', 'barbosa', 'dacumos', 'vhie', 'notario', 'diko', 'jvr', 'dan', 'jadloc', 'tanzie', 'flordeliza', 'caampued', 'cendy', 'baillo', 'alojchristine', 'dalusong', 'adri', 'odee', 'son', 'rhym', 'bryan', 'vidal', 'ruby', 'usman', 'jenina', 'james', 'tere', 'fhei', 'l', 'alexis', 'nerecena', 'cammille', 'wong', 'jefferson', 'mead', 'lheyann', 'bong', 'alice', 'deguzman', 'em', 'guinto', 'jenn', 'rachelle', 'cecille', 'rojas', 'alojadoacatherine', 'katrina', 'sardeniola', 'guilangue', 'macabanti-geronimo', 'marcos', 'girl', 'nanit', 'aldrin', 'marius', 'angulo', 'rey', 'ibarra', 'ernie', 'garcia', 'gonzales', 'robert', 'pajiji', 'kenn', 'keno', 'lagumbay', 'mandz', 'zanchez', 'charlyne', 'daniel', 'ren', 'dominguiano', 'gutierrez', ',buan', 'generoso', 'dahleng', 'lorgene', 'ella', 'rj', 'benjamin', 'torres', 'harold', 'clarence', 'alban', 'lawrence', 'ganzon', 'caronan', 'perucho', 'fred', 'mikhail', 'jhenni', 'jill', 'yuri', 'carl', 'ramoy', 'asi', 'romualdo', 'ariane', 'princess', 'esteves', 'asmaira', 'marla', 'yara', 'dorlyn', 'ate', 'watisdis', 'g', 'cañeda', 'cadiz', 'barbara', 'helen', 'gelyn', 'marlo', 'david', 'katniss', 'nalzaro', 'mae', 'isa', 'quinto', 'tyntine', 'legaspi', 'nebrida', 'cangas', 'paclibar', 'albarido', 'pangilinan', 'dione', 'justine', 'ong', 'famor', 'jesus', 'bernadette', 'pamparo-castrillolouise', 'mel', 'jazz', 'pablo', 'rona', 'jerizza', 'scent', 'mervyn', 'lazala', 'reinier', 'combate', 'ian', 'castaneda', 'castillo', 'imelda', 'perado', 'isadel', 'pilarca', 'magcawas', 'ramssel', 'aldwin', 'patiño', 'mayvelle', 'gilbert', 'john', 'jen', 'genesis', 'rosario', 'cabral', 'vargasmaglalang', 'padrinao-villanueva', 'acogido', 'taylo-', 'villanueva', 'silang', 'carmi', 'valencia', 'grace', 'valdz', 'rollie', 'king', 'vienne', 'man-on', 'jayjay', 'treb', 'maricel', 'manlapaz', 'capili', 'cristobal', 'abs-cbn', 'genson', 'salazar', 'lourdes', 'sophia', 'and', 'ver-dee', 'jinky', 'aquino', 'ana', 'lhene', 'ann', 'ram', 'francial', 'dungog-romagos', 'canlapan', 'mararac', 'quilinguing', 'herlene', 'kevin', 'ray', 'poblete', 'sotelo', 'ybanez', 'lamsen', 'maximo', 'mia', 'lim', 'ecalnir', '-', 'oh', 'roehl', 'aisha', 'chiong', 'fajilan', 'rowen', 'arazas', 'jhen', 'fayot', 'emalyn', 'mamhie', 'santiago', 'mariz', 'abella', 'manette', 'alcantara', 'unang', 'hazel', 'maris', 'jeph', 'jazziel', 'kelly', 'caponpon', 'sapo', 'charm', 'villafuerte', 'bh3', 'marie', 'fria', 'maria', 'don', 'besas', 'ofiana', 'flor', 'ylime', 'm', 'paru', 'saguinsin', 'lujera', 'bulan', 'charmaeine', 'brey', 'renier', 'gabaleo', 'ramososhasha', 'daluz', 'arjaybaluyot', 'zacarias', 'ralph', 
         'charles', 'niel', 'jarder', 'troy', 'merin', 'perlas', 'sarenbeniga', 'cabeliza', 'sangalang', 'florentino', 'kale', 'figueroa', 'cyril', 'leigh', 'cherryl', 'jay', 'jabee', 'locsin', 'ayen', 'mitzi', 'tanya', 'aldo', 'botabara', 'alocha', 'jam', 'gideon', 'aby', 'vierneza', 'caroline', 'sieg', 'ruiz', 'rica', 'boris', 'angieline', 'adviento', 'couz', 'jomar', 'criste', 'de', 'dc', 'b', 'cora', 'dy', 'uy', 'kayganda', 'gen', 'rondez', 'alexander', 'buan', 'dianne', 'casabuena', 'joanne', 'emm', 'corvin', 'lala', 'remata', 'charleane', 'felipe', 'jaime', 'roger', 'aris', 'jeosh', 'allito', 'dagtaagta', 'leynes', 'bam', 'jovie', 'khristine', 'rfl', 'carrillo', 'eiram', 'nixx', 'agulto', 'cao', 'buscagan', 'isabel', 'roque', 'ablen', 'leslie', 'rmg', 'ricyet', 'bautista', 'troilus', 'nimfa', 'angie', 'corro', 'caster', 'cheska', 'dexter', 'jennyrose', 'mitch', 'gayjow', 'apol', 'arlyn', 'mamayay', 'verbo', 'rito', 'aranza', 'isha', 'morales', 'marvin', 'zabala', 'palogan', 'jasmin', 'baltar', 'tania', 'dhianne', 'rimas', 'jov', 'domo', 'joy', 'herrera', 'valerie', 'antoniano', 'jr', 'hirit', 'javierariane', 'nikka', 'manalili', 'yba', 'selene', 'news', 'ravela', 'lopez', 'loudine', 'manabat', 'c', 'javier', 'almonguera', 'jm', 'jocelyn', 'edgar', 'vincharl', 'shankanecai', 'soriano', 'tolentino', 'milo', 'jonas', 's', 'com', 'eto', 'con', 'ayeeh', 'oswa', 'mangilit', 'co', 'jeff', 'toni', 'cinth', 'durante', 'cla', 'guzman', 'karen', 'rae', 'esbra', 'kev', 'baccay', 'magbanua', 'sherwin', 'san', 'carpio', 'rrvee', 'kinjan', 'karlo', 'lanymay', 'odey', 'karla', 'elmer', 'teus', 'kasten', 'mark', 'olave', 'raffy', 'mikee', 'yan', 'noel', 'razzie', 'pj', 'quintong', 'zobel', 'mary', 'caloi', 'hernandez', 'roselyn', 'mike', 'cecile', 'dhey', 'chua', 'gemma', 'mahusay', 'dhes', 'andrew', 'gan', 'fritz', 'andrei', 'dote', 'taboadabas', 'mhee', 'quilapio', 'aileen', 'kerstin', 'judee', 'remy', 'deden', 'cepriano', 'calderonukaren', 'castro', 'n', 'dacanay', 'capinpin', 'aldie', 'margie', 'maravilla-casacop', 'vicky', 'jerald', 'drewan', 'archie', 'veronica', 'parugrug', 'bustarde', 'portugal', 'susana', 'cabangon', 'veras', 'shamy', 'yam', 'ii', 'rio', 'oquindo', 'majano', 'perez', 'jingco', 'zandro', 'boom', 'zaldy', 'ayuban', 'ignacio', 'santos', 'guzman-francisco', 'cascabel', 'pau', 'aldana', 'belle', 'edwin', 'macalalad', 'bella', 'leoniño', 'rules', 'ocampo', 'jepher', 'naces', 'claridad', 'miya', 'pam', 'paoner', 'brigente', 'calacday', 'raymond', 'leonie', 'condes', 'talaban', 'kit', 'palabrica', 'cudiamat', 'kim', 'dayan', 'villegas', 'vargas', 'gaspay', 'villa', 'arra', 'albesa', 'blanco', 'meazel', 'antonio', 'portillo', 'jessica', 'toy', 'espiritu', 'llanto', 'jayvee', 'legera', 'denjie', 'burgos', 'alvin', 'bonecille', 'jexter', 'rhoen', 'hervas', 'celzo', 'bes', 'jaul', 'oxford', 'jonard', 'ethel', 'patsy', 'laurel', 'paul', 'montañez', 'riachelle', 'rochelle', 'trins', 'bry', 'rose', 'gma', 
         'gorme', 'tin', 'balubar', 'rubio', 'bobis', 'samuel', 'tuway', 'viansuaverdez', 'ada', 'bagacina', 'yopo', 'panara-ag', 'alcala', 'venzon', 'jake', 'clirkz', 'sunico', 'vanessa', 'granados', 'sabdaniaira', 'cruz', 'recy', 'malubay', 'tolentino-miano', 'alida', 'lanie', 'enriquez', 'mariah', 'margiemel', 'popoy', 'rozend', 'christine', 'verner', 'paradagomez', 'salinas', 'edjen', 'cayabyab', 'arthur', 'gumana', 'rhodora', 'talosig', 'martin', 'ivan', 'mamagat', 'chico', 'love', 'salih', 'dimapilis', 'manaay', 'lazarte', 'macario', 'shen', 'chrissele', 'tulod', 'denice', 'nagal', 'donald', 'francisco', 'rhazel', 'gracia', 'dimaano', 'cebrero', 'bagtas', 'alfaize', 'marzan', 'caredz', 'manahan', 'isagan', 'cavada', 'masaybeng', 'irma', 'rmarie', 'bagos', 'jelka', 'mhendie', 'oblanca', 'cnn', 'anne', 'dizon', 'marit', 'anna', 'arnel', 'mante', 'sarah', 'abanes', 'emms', 'gmax', 'briones', 'bogie', 'reza', 'palisoc', 'marquez', 'rosal', 'oliver', 'pascual', 'yolly', 'ross', 'francis', 'diosa', 'russell', 'shine', 'conrad', 'cerafica', 'justin', 'adzwiya', 'linsangan', 'jay-ar', 'o', 'hilarion', 'wolf', 'kpn', 'tomo', 'segovia', 'maurin', 'hazey', 'dulay', 'reycie', 'carolyn', 'costumbrado', 'obrero', 'miranda', 'catherine', 'retchie', 'gleng', 'yap', 'martinez', 'lacerna', 'paches', 'magbitang', 'mauie', 'diala', 'joyce', 'arvin', 'gomez', 'cajeta', 'joemar', 'jing', 'qadriyyah', 'delos', 'ortiz', 'neser', 'pauline', 'loo', 'ponce', 'imperial', 'joseph', 'daniell', 'shella', 'dioso', 'jayron', 'jane', 'pilares', 'labaco', 'gil', 'dutchque', 'vicente', 'pauyon', 'bobadilla', 'gulmatico', 'vasquez', 'arceta', 'kristian', 'jun', 'mc', 'marge', 'concepcion', 'mercado', 'funda', 'lans', 'pepperminty', 'khim', 'jumawid', 'ladines', 'alvero', 'kiitt', 'erick', 'paires', 'salome', 'angcao', 'maglalang', 'merilyn', 'manuel', 'taguibao', 'madz', 'bermas', 'krizzie', 'molato', 'kathy', 'ae', 'chad', 'ghaneza', 'sarsola', 'russelle', 'draculan', 'al', 'añonuevo', 'au', 'lher', 'aristotle', 'kho', 'abarilla', 'grafil', 'lyn', 'claudine', 'eric', 'fajie', 'ronil', 'tita', 'polangco', 'guarin', 'evilla', 'sumampong', 'quinjacob', 'abigail', 'lendy', 'nick', 'jona', 'feliciano', 'nico', 'oscar', 'rosalita', 'njie', 'rigonan', 'riam', 'garcera', 'tess', 'cyrmyn', 'jestoni', 'cabrera', 'chavez', 'ku', 'iza', 'janella', 'papa', 'acosta', 'medina', 'regalario', 'margaret', 'maureen', 'macallop', 'lacaba', 'abanes-escalona', 'terry', 'sai-rex', 'cabuang', 'valderama', 'urbano', 'jones', 'miles', 'sayson', 'news5', 'geraldine', 'hadap', 'dumalag', 'krystyn', 'aiko', 'elizalde', 'dinia']

	names_db = Names()
	names_db.name_list = names
	names_db.save()

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
			#df = extract.searchKeyWord(searchform.cleaned_data['keyword'])[0]
			pickling = os.path.join(settings.BASE_DIR, "SMAApp\\pkls\\SM.pkl")
			#df.to_pickle(pickling)
			df = pd.read_pickle(pickling)

			# df = pd.DataFrame(data)
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
			formatted_quick_stats = format_quick_stats_comma(quick_stats_data)

			quick_stats = formatted_quick_stats
			request.session["quick_stats"] = quick_stats
			diag_chartdata = {}
			request.session['chartdata'] = prepare_chartdata(df)
			print("chart data size: ", sys.getsizeof(request.session['chartdata']))
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
    # chartdata = {}
	chartdata = ChartData()
    # Data for timeline linechart (Diagnostics Page)
	chartdata.timeline = engagements.return_timeline(df)
    # chartdata["timeline"] = engagements.return_timeline(df)

    # Data for source donut chart (Diagnostics Page)
	chartdata.source =  engagements.return_source(df)
    # chartdata["source"] = engagements.return_source(df)

    # Data for composition donut chart (Diagnostics Page)
	chartdata.composition = engagements.return_composition(df)
    # chartdata["composition"] = engagements.return_composition(df)

    # Data for hashtags barchart (Topics Page)
	chartdata.hashtags = hashtags.hash_(df)
    # chartdata["hashtags"] = hashtags.hash_(df)

    # Data for polarity donut chart (Sentiments Page)
	chartdata.sentiments = engagements.return_polarity_chartdata(df)
    # chartdata["sentiments"] = engagements.return_polarity_chartdata(df)
	chartdata.polarity_table = engagements.return_polarity(df)
    # chartdata["polarity_table"] = engagements.return_polarity(df)

	return chartdata

def login_user(request):
	if request.method == 'POST':
		loginform = LoginForm(request.POST)
		if loginform.is_valid():
			email =  loginform.cleaned_data.get('email')
			password = loginform.cleaned_data.get('password')
			user1 = authenticate(email=email,password=password)
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
				print("inside try")
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
					# return HttpResponseRedirect('/diagnostics/')
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

# def revoke_started_task():
# 	# isSnapshots values 'true' and 'false' is string
# 	# so it will be boolean when passed to js on other functions
# 	if request.session['isSnapshot'] == 'true' and request.session['lda_data']:

def open_registration(request):
	loginform = LoginForm()
	registrationform = RegistrationForm()
	searchform = SearchForm()
	if request.session.get('isloggedin'):
		return HttpResponseRedirect('/diagnostics/')
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
				return HttpResponseRedirect('/diagnostics/')
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
				for snapshotObj in Snapshot.objects(_id=snapshot_id):
					logging.info("Iterating data using snapshot id: %s", snapshot_id)
					request.session['search_keyword'] = snapshotObj.keyword
					request.session['df'] = pd.DataFrame(snapshotObj.extracted_data)
					# chartdata = {}
					chartdata = ChartData()
					chartdata.timeline = pd.DataFrame(snapshotObj.chart_data[0]['timeline']).to_dict('list')
					chartdata.source = pd.DataFrame(snapshotObj.chart_data[0]['source']).to_dict('list')
					chartdata.composition = pd.DataFrame(snapshotObj.chart_data[0]['composition']).to_dict('list')
					chartdata.hashtags = snapshotObj.chart_data[0]['hashtags']
					chartdata.sentiments = pd.DataFrame(snapshotObj.chart_data[0]['sentiments']).to_dict('list')
					chartdata.polarity_table = snapshotObj.chart_data[0]['polarity_table'][0] # Access the dict inside the list thats why theres another [0] after the polarity table
					# chartdata['timeline'] = pd.DataFrame(snapshotObj.chart_data[0]['timeline']).to_dict('list')
					# chartdata['source'] = pd.DataFrame(snapshotObj.chart_data[0]['source']).to_dict('list')
					# chartdata['composition'] = pd.DataFrame(snapshotObj.chart_data[0]['composition']).to_dict('list')
					# chartdata['hashtags'] = snapshotObj.chart_data[0]['hashtags']
					# chartdata['sentiments'] = pd.DataFrame(snapshotObj.chart_data[0]['sentiments']).to_dict('list')
					# chartdata['polarity_table'] = snapshotObj.chart_data[0]['polarity_table'][0] # Access the dict inside the list thats why theres another [0] after the polarity table
					request.session['chartdata'] = chartdata
					diag_chartdata = create_diag_chartdata(chartdata)
					request.session['diag_chartdata'] = diag_chartdata

					# Returns a list of insights
					insights_fromdb = snapshotObj.insights
					# Extract insights from list of insights
					if insights_fromdb is not None:
						for idx, insights in enumerate(insights_fromdb):
							insight[idx] = insights

					# wc_image = snapshotObj.wordcloud_image.read()
					# wc_image_content_type = snapshotObj.wordcloud_image.content_type
					quick_stats_data = snapshotObj.quick_stats
					request.session['quick_stats_db'] = quick_stats_data
					request.session['influencers_data'] = snapshotObj.influencers_data
					request.session['influential_data'] = snapshotObj.influential_data
					request.session['quick_stats'] = format_quick_stats_comma(quick_stats_data)
					
					# PIL Image way 
					# print("snapshotObj.wordcloud_image", snapshotObj.wordcloud_image.width)
					request.session['wc_image_str'] = utils.convert_to_base64(snapshotObj.wordcloud_image.read())
					# request.session['wc_image_str'] = utils.convert_to_base64(snapshotObj.wordcloud_image)
					# Base64 way
					# request.session['wc_image_str'] = snapshotObj.wordcloud_image
					snapshot_lda_data = utils.restore_lda_keynames(snapshotObj.lda_data)
					request.session["lda_data"] = snapshot_lda_data
				
				# snapshotlistform = SnapshotListForm(initial={'max_number': '3'})
				request.session['selected_snapshot'] = snapshot_id
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
	diag_chartdata.timeline = timeline_linechart(chartdata.timeline)
	diag_chartdata.source = sourcePiechartConverter(chartdata.source)
	diag_chartdata.composition = compositionPiechartConverter(chartdata.composition)
	# diag_chartdata["timeline"] = timeline_linechart(chartdata.timeline)
	# diag_chartdata["source"] = sourcePiechartConverter(chartdata.source)
	# diag_chartdata["composition"] = compositionPiechartConverter(chartdata.composition)
	return diag_chartdata

# Returns lat, lang, user, tweet
def return_geocode(request):
	geoCodes = engagements.return_geocode(request.session["df"])
	return JsonResponse(geoCodes)  

def generate_wordcloud_image(request):
	# image_filename = "wordcloud-" + request.session["user_id"] + ".png"
	# image_path = os.path.join(settings.BASE_DIR, "SMAApp\\static\\images\\wordcloud\\" + image_filename)
	if request.session['isSnapshot'] != 'true':
		# if not os.path.isfile(image_path):
		print("image not in path")
		pil_img_str = wordcloudscript.return_wordcloud(request.session["df"])
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
    df = request.session["df"]
    lda_task_id = tasks.generate_lda_data.delay(df.to_json())
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
			tempImgObj = utils.create_temp_img_file(request.session['pil_image_str'])
			snapshot.wordcloud_image.put(tempImgObj, content_type='image/png')

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
	
	# return HttpResponseRedirect('/diagnostics/')
	# return render(request, 'diagnostics.html',
    #            {'quick_stats':quick_stats,
	# 		   'diag_chartdata':diag_chartdata,
	# 		   'searchform':searchform,
	# 		   'snapshotlistform':snapshotlistform,
	# 		   'loginform':loginform,
	# 		   'username':globals.loggedin_username})

def start_background_tasks(request):
	df = request.session["df"]
	request.session["sentiments_data_id"] = tasks.generate_sentiments_data.delay(df.to_json())
	request.session["lda_data_id"] = tasks.generate_lda_data.delay(df.to_json())
	request.session.save()

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
		data['polar'] = polarity_donutchart(chartdata.sentiments)
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
	if request.method == 'POST':
		get_keyword(request)
	else:
		data = {}
		# data["barchart"] = request.session["chartdata"]["hashtags"]
		chartdata = request.session['chartdata']
		data["barchart"] = chartdata.hashtags
		# data["barchart"] = demo_horizontalBarChart(chartdata)
         
		sessionid = request.session["user_id"]
				#path = "C:/Users/christian.dy/Documents/GitHub/SMALab/SMAProject/SMAApp/templates/lda/"
		#imagePath = "C:/Users/christian.dy/Documents/GitHub/SMALab/SMAProject/SMAApp/static/images/wordcloud/"
		
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

def format_quick_stats_comma(data):
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
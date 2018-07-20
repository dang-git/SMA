from django import forms
from SMAApp.models import Snapshot, User
from SMAApp import queries, globals, smaapp_constants
class SearchForm(forms.Form):
	keyword = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter keyword/keywords separated by comma','id': 'id_keyword'}))

 #[(snapshotObj._id,snapshotObj.snapshot_name) for snapshotObj in Snapshot.objects(owner='Dy')]

class SnapshotListForm(forms.Form):
	snapshotchoices = forms.ChoiceField()
	# Override init method to set dropdown values on every form load
	def __init__(self, *args, **kwargs):
		super(SnapshotListForm, self).__init__(*args, **kwargs)
		self.fields['snapshotchoices'].choices = queries.get_snapshot_list() #forms.ChoiceField(choices=globals.SNAPSHOT_LIST)
		# self.fields['snapshotchoices'] = forms.ModelChoiceField(queryset=Snapshot.objects.all(),empty_label="")

class RegistrationForm(forms.Form):
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Username','id': 'id_username'}))
	email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email','id': 'id_email'}))
	password = forms.CharField(widget=forms.PasswordInput())
	address = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Address','id': 'id_address'}))
	license_type = forms.ChoiceField(choices=smaapp_constants.LICENSE_TYPES)
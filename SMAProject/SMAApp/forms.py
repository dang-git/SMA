from django import forms
from SMAApp.models import Snapshot, User
from SMAApp import queries, globals, smaapp_constants
class SearchForm(forms.Form):
	keyword = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter keyword/keywords separated by comma','id': 'id_keyword'}))

 #[(snapshotObj._id,snapshotObj.snapshot_name) for snapshotObj in Snapshot.objects(owner='Dy')]

class SnapshotListForm(forms.Form):
	# Override init method to set dropdown values on every form load
	def __init__(self, *args, **kwargs):
		request = kwargs.pop("request",None)
		super(SnapshotListForm, self).__init__(*args, **kwargs)
		if request is not None:
			if request.session.get('loggedin_userid'):
				self.fields['snapshotchoices'] = forms.ChoiceField()
				self.fields['snapshotchoices'].widget.attrs = {'class':'snapshot-choices'}
				self.fields['snapshotchoices'].choices = request.session['snapshot_list'] #queries.get_snapshot_list(request.session['loggedin_userid']) #forms.ChoiceField(choices=globals.SNAPSHOT_LIST)		
			if request.session.get('selected_snapshot'):
				self.fields['snapshotchoices'].initial = [request.session['selected_snapshot']]
				# self.fields['snapshotchoices'].widget.choices = queries.get_snapshot_list(request.session['loggedin_userid']) #forms.ChoiceField(choices=globals.SNAPSHOT_LIST)		
		# self.fields['snapshotchoices'] = forms.ModelChoiceField(queryset=Snapshot.objects.all(),empty_label="")

class RegistrationForm(forms.Form):
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'registration-input','id': 'reg_username_id'}))
	email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'registration-input','id': 'reg_email_id'}))
	password = forms.CharField(label= '', widget=forms.PasswordInput(attrs={'class': 'registration-input','id': 'reg_password_id'}))
	address = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'registration-input','id': 'reg_address_id'}))
	license_type = forms.ChoiceField(choices=smaapp_constants.LICENSE_TYPES)

class LoginForm(forms.Form):
	email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email','id': 'login_email_id'}))
	password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password','id': 'login_password_id'}))

# class SaveSnapshotForm(forms.Form):
# 	snapshot_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'snapshot-name-input','id': 'snapshot_name_id'}))
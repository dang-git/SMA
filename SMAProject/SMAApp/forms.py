from django import forms
from SMAApp.models import Snapshot, User
from SMAApp import queries, globals
class SearchForm(forms.Form):
	keyword = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter keyword/keywords separated by comma','id': 'id_keyword'}))

 #[(snapshotObj._id,snapshotObj.snapshot_name) for snapshotObj in Snapshot.objects(owner='Dy')]

class SnapshotListForm(forms.Form):
	# Override init method to set dropdown values on every form load
	def __init__(self, *args, **kwargs):
		super(SnapshotListForm, self).__init__(*args, **kwargs)
		self.fields['snapshotchoices'] = forms.ChoiceField(choices=globals.SNAPSHOT_LIST)
	# choice = forms.ModelChoiceField(queryset=Snapshot.objects.all(),empty_label="")
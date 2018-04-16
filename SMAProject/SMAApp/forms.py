from django import forms

class SearchForm(forms.Form):
	keyword = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter keyword/keywords separated by comma','id': 'id_keyword'}))
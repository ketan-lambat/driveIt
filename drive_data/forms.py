from django import forms
from .models import FileTest


class UploadFileForm(forms.ModelForm):
	class Meta:
		model = FileTest
		fields = ['file']

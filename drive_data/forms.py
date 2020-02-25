from django import forms
from .models import File_Test


class UploadFileForm(forms.ModelForm):
	class Meta:
		model = File_Test
		fields = {'name', 'file'}

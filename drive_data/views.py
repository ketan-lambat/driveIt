from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm
from .models import File_Test


class Home(TemplateView):
	template_name = 'base.html'


def upload(request):
	context = {}
	if request.method == 'POST':
		uploaded_file = request.FILES['document']
		fs = FileSystemStorage()
		file_name = fs.save(uploaded_file.name, uploaded_file)
		context['url'] = fs.url(file_name)
	return render(request, 'upload/simple_upload.html', context)


def file_list(request):
	files = File_Test.objects.all()
	return render(request, 'upload/file_list.html', {
		'files':files
	})


def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('file_list')
	else:
		form = UploadFileForm
	return render(request, 'upload/upload_file.html', {
		'form': form
	})

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
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
		'files': files
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


def delete_book(request, pk):
	if request.method == 'POST':
		file = File_Test.objects.get(pk=pk)
		file.delete()
	return redirect('file_list')


class FileListView(ListView):
	model = File_Test
	template_name = 'upload/file_list.html'
	context_object_name = 'files'


class UploadFileVIew(CreateView):
	model = File_Test
	form_class = UploadFileForm
	success_url = reverse_lazy('class_file_list')
	template_name = 'upload/upload_file.html'

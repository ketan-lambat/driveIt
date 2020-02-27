from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from .forms import UploadFileForm
from .models import FileTest


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
	files = FileTest.objects.all()
	return render(request, 'upload/file_list.html', {
		'files': files
	})


def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		# print(request.FILES)
		if form.is_valid():
			a = form.save()
			f_name = request.FILES['file'].name
			f_size = request.FILES['file'].size
			a.name = f_name
			a.size = f_size/1024
			a.save()
			# print(f_name)
		return redirect('file_list')
	else:
		form = UploadFileForm
		return render(request, 'upload/upload_file.html', {
			'form': form
		})


def delete_book(request, pk):
	if request.method == 'POST':
		file = FileTest.objects.get(pk=pk)
		file.delete()
	return redirect('file_list')


class FileListView(ListView):
	model = FileTest

	@staticmethod
	def file_name(self, request):
		if request.method == 'POST':
			f_name = request.FILES['uploaded_file'].name
			print(f_name)

	template_name = 'upload/file_list.html'
	context_object_name = 'files'


class UploadFileVIew(CreateView):
	model = FileTest
	form_class = UploadFileForm

	def file_name(self, request):
		if request.method == 'POST':
			f_name = request.FILES['uploaded_file'].name
			print(f_name)

	success_url = reverse_lazy('class_file_list')
	template_name = 'upload/upload_file.html'

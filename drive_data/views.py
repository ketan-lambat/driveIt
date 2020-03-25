from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlunquote as urldecode
from django.views.generic import TemplateView, ListView, CreateView, View

from .forms import UploadFileForm
from .models import File, Folder
from .models import FileTest


class Home(TemplateView):
    template_name = 'basic.html'


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
            a.size = f_size / 1024
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


# Final Drive Views:


class DriveDataView(LoginRequiredMixin, View):
    def get(self, request):
        context = dict()
        drive = request.user.drive
        context['files'] = drive.files.all()
        context['folders'] = drive.files_folder.all()
        return render(request, 'drive_data/drive_home.html', context=context)


class FolderDataView(LoginRequiredMixin, View):
    def get(self, request, path):
        path = path.split('/')
        user = request.user
        parent = Folder.objects.get(drive_user=user)
        paths = []
        for i in range(len(path)):
            paths.append((urldecode(path[i]), '/'.join(path[:i + 1])))
        for folder in map(urldecode, path):
            try:
                parent = parent.files_folder.get(name=folder)
            except:
                return HttpResponse("Not found")
        context = {'files': parent.files.all(),
                   'folders': parent.files_folder.all(),
                   'paths': paths,
                   'current_path': '/'.join(path)}

        return render(request, 'drive_data/folder_data.html', context=context)


def get_parent(user, path):
    parent = Folder.objects.get(drive_user=user)
    if path not in ['/', '']:
        for folder in map(urldecode, path.split('/')):
            try:
                parent = parent.files_folder.get(name=folder)
            except:
                raise ValueError
    return parent


@login_required
def file_upload_view(request, path):
    try:
        parent = get_parent(request.user, path)
    except ValueError:
        return HttpResponse("Not found")
    print(request.POST)
    try:
        f = request.FILES['file']
    except:
        return HttpResponse("Unable to process file")
    if File.objects.filter(name=f.name, location=parent).count() > 0:
        return HttpResponse("A file with that name already exists.")
    file = File.objects.create(name=f.name, file_size=f.size,
                               author=request.user, file=request.FILES['file'],
                               location=parent)
    if parent == request.user.drive:
        return redirect('drive_home')
    return redirect('folder_data', path=path)


@login_required
def create_folder_view(request, path):
    try:
        parent = get_parent(request.user, path)
    except ValueError:
        return HttpResponse("Not found")

    try:
        f_name = request.POST['folder_name']
    except:
        return HttpResponse("Enter Folder Name")
    if Folder.objects.filter(name=f_name, location=parent).count() > 0:
        return HttpResponse("Folder Already Exists")
    folder = Folder.objects.create(name=f_name, author=request.user, location=parent)
    return redirect('folder_data', path=folder.urlpath)


@login_required
def file_delete_view(request, pk):
    if request.method == "POST":
        try:
            file = File.objects.get(author=request.user, pk=pk)
            parent = file.location
            file.delete()
        except:
            return HttpResponse("File does not exist.")
        if parent and parent.urlpath != '':
            return redirect('folder_data', path=parent.urlpath)
    else:
        return HttpResponse("NOT ALLOWED")
    return redirect('drive_home')


@login_required
def folder_delete_view(request, pk):
    if request.method == "POST":
        try:
            folder = Folder.objects.get(author=request.user, pk=pk)
            parent = folder.location
            folder.delete()
        except:
            return HttpResponse("Folder does not exist.")
        if parent and parent.urlpath != '':
            return redirect('folder_data', path=parent.urlpath)
    else:
        return HttpResponse("NOT ALLOWED")
    return redirect('drive_home')

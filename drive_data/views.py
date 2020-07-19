from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlunquote as urldecode
from django.views.generic import TemplateView, View
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drive_data.models import File, Folder
from uploads.models import Upload


class Home(TemplateView):
    template_name = "basic.html"


# Final Drive Views:


class DriveDataView(LoginRequiredMixin, View):
    def get(self, request):
        context = dict()
        drive = request.user.drive
        context["files"] = drive.files.all()
        context["folders"] = drive.files_folder.all()
        return render(request, "drive_data/drive_home.html", context=context)


class FolderDataView(LoginRequiredMixin, View):
    def get(self, request, path):
        print(path)
        if path in [None, '', '/', '//']:
            return redirect('drive_home')
        path = path.split("/")
        user = request.user
        parent = Folder.objects.get(drive_user=user)
        paths = []
        for i in range(len(path)):
            paths.append((urldecode(path[i]), "/".join(path[: i + 1])))
        for folder in map(urldecode, path):
            try:
                parent = parent.files_folder.get(name=folder)
            except:
                return HttpResponse("Not found")
        context = {
            "files": parent.files.all(),
            "folders": parent.files_folder.all(),
            "paths": paths,
            "current_path": "/".join(path),
        }

        return render(request, "drive_data/folder_data.html", context=context)


def get_parent(user, path):
    parent = Folder.objects.get(drive_user=user)
    if path not in ["/", ""]:
        for folder in map(urldecode, path.split("/")):
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
        f = request.FILES["file"]
    except:
        return HttpResponse("Unable to process file")
    if File.objects.filter(name=f.name, location=parent).count() > 0:
        return HttpResponse("A file with that name already exists.")
    file = File.objects.create(
        name=f.name,
        file_size=f.size,
        author=request.user,
        file=f,
        location=parent,
    )
    if parent == request.user.drive:
        return redirect("drive_home")
    return redirect("folder_data", path=path)


@login_required
def streaming_file_upload_create(request):
    if request.method == 'GET':
        return HttpResponse(status=405)
    try:
        print(request.POST)
        path = request.POST['path']
        parent = get_parent(request.user, path)
    except ValueError:
        return HttpResponse("Not found")
    from uploads.models import Upload

    u = Upload.objects.create(
        upload_length=request.POST['file_size'],
        filename=request.POST['filename'],
    )
    file = File.objects.create(
        name=request.POST['filename'],
        file_size=request.POST['file_size'],
        author=request.user,
        file=None,
        location=parent,
        temp_file_id=u.guid,
    )

    return redirect(reverse('streaming_upload', kwargs={'guid': str(u.guid)}))


@login_required
def create_folder_view(request, path):
    try:
        parent = get_parent(request.user, path)
    except ValueError:
        return HttpResponse("Not found")

    try:
        f_name = request.POST["folder_name"]
    except:
        return HttpResponse("Enter Folder Name")
    if Folder.objects.filter(name=f_name, location=parent).count() > 0:
        return HttpResponse("Folder Already Exists")
    folder = Folder.objects.create(
        name=f_name, author=request.user, location=parent
    )
    return redirect("folder_data", path=folder.urlpath)


@login_required
def file_delete_view(request, pk):
    if request.method == "POST":
        try:
            file = File.objects.get(author=request.user, pk=pk)
            parent = file.location
            file.delete()
        except:
            return HttpResponse("File does not exist.")
        if parent and parent.urlpath != "":
            return redirect("folder_data", path=parent.urlpath)
    else:
        return HttpResponse("NOT ALLOWED")
    return redirect("drive_home")


@login_required
def folder_delete_view(request, pk):
    if request.method == "POST":
        try:
            folder = Folder.objects.get(author=request.user, pk=pk)
            parent = folder.location
            folder.delete()
        except:
            return HttpResponse("Folder does not exist.")
        if parent and parent.urlpath != "":
            return redirect("folder_data", path=parent.urlpath)
    else:
        return HttpResponse("NOT ALLOWED")
    return redirect("drive_home")


@csrf_exempt
@login_required
def streaming_file_upload(request, guid):
    try:
        u = Upload.objects.get(guid=guid)
        f = File.objects.get(temp_file_id=guid)
    except Upload.DoesNotExist:
        return HttpResponse("Not found")
    except File.DoesNotExist:
        return HttpResponse("Not Found")

    context = {
        'upload_url': reverse('uploads:api:upload-detail',
                              kwargs={'guid': f.temp_file_id})
    }
    return render(request, 'upload/streaming_upload.html', context=context)

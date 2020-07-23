from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from drive_data.models import Item
from drive_data.zip import make_tmp_archive
from registration.models import User
from .models import SharedItem
import os


@login_required
def share_item(request, item_id):
    # noinspection PyGlobalUndefined
    global item
    if request.method == 'GET':
        users = User.objects.exclude(username=request.user.username)
        try:
            item = Item.objects.get(author=request.user, pk=item_id)
            shared = SharedItem.objects.get(item=item)
            context = {'shared': shared, 'item': item, 'users': users}
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        except SharedItem.DoesNotExist:
            context = {'item': item, 'shared': None, 'users': users}
        return render(request, 'share/share.html', context=context)
    elif request.method == 'POST':
        print(request.POST)
        users = User.objects.exclude(username=request.user.username)
        try:
            item = Item.objects.get(author=request.user, pk=item_id)
            shared = SharedItem.objects.get(item=item)
            access_type = SharedItem.Permission.PUBLIC if request.POST.get(
                'type') == '1' else SharedItem.Permission.SELECTIVE
            shared.permission = access_type
            shared.save()
            if access_type == SharedItem.Permission.SELECTIVE:
                for username in request.POST.get('users', []):
                    try:
                        user = User.objects.get(username=username)
                        shared.access_user.add(user, bulk=False)
                    except:
                        pass
            shared.save()
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        except SharedItem.DoesNotExist:
            access_type = SharedItem.Permission.PUBLIC if request.POST.get(
                'type') == '1' else SharedItem.Permission.SELECTIVE
            shared = SharedItem.objects.create(item=item, permission=access_type)
            shared.save()
            if access_type == SharedItem.Permission.SELECTIVE:
                for username in request.POST.get('users', []):
                    try:
                        user = User.objects.get(username=username)
                        shared.access_user.add(user, bulk=False)
                    except:
                        pass
            shared.save()
        context = {'shared': shared, 'item': item, 'users': users}
        return render(request, 'share/share.html', context=context)


def shared_item_view(request, guid):
    try:
        shared = SharedItem.objects.get(public_id=guid)
    except SharedItem.DoesNotExist:
        return HttpResponse(status=404)
    if shared.permission == SharedItem.Permission.SELECTIVE:
        if request.user.is_anonymous:
            return HttpResponse(status=401)
        elif request.user not in shared.access_user.all():
            return HttpResponse(status=403)

    if hasattr(shared.item, 'drive_file'):
        return render(request, 'share/view.html', context={'shared': shared})
    else:
        return render(request, 'share/view.html',
                      context={'shared': shared, 'is_folder': True,
                               'folders': shared.item.drive_folder.files_folder.all,
                               'files': shared.item.drive_folder.files.all})


def shared_folder_view(request, guid, item_id):
    try:
        shared = SharedItem.objects.get(public_id=guid)
    except SharedItem.DoesNotExist:
        return HttpResponse(status=404)
    if shared.permission == SharedItem.Permission.SELECTIVE:
        if request.user.is_anonymous:
            return HttpResponse(status=401)
        elif request.user not in shared.access_user.all():
            return HttpResponse(status=403)

    if hasattr(shared.item, 'drive_file'):
        return HttpResponse(status=400, content="Invalid URL")
    else:
        try:
            view_folder = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return HttpResponse(status=400, content="Invalid URL")
        if not hasattr(view_folder, 'drive_folder'):
            return HttpResponse(status=400, content="Invalid URL")
        return render(request, 'share/view.html',
                      context={'shared': shared, 'is_folder': True,
                               'folders': view_folder.drive_folder.files_folder.all,
                               'files': view_folder.drive_folder.files.all})


def download_file(request, guid, item_id):
    try:
        shared = SharedItem.objects.get(public_id=guid)
    except SharedItem.DoesNotExist:
        return HttpResponse(status=404)
    if shared.permission == SharedItem.Permission.SELECTIVE:
        if request.user.is_anonymous:
            return HttpResponse(status=401)
        elif request.user not in shared.access_user.all():
            return HttpResponse(status=403)
    if hasattr(shared.item, 'drive_folder'):
        try:
            shared_item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return HttpResponse(status=400, content="Invalid URL")
        if shared_item.has_parent(shared.item.pk):
            download_item = shared_item
        else:
            return HttpResponse(status=403, content="You cannot access this item")
    else:
        if item_id == shared.item.pk:
            download_item = shared.item
        else:
            return HttpResponse(status=400, content="Invalid URL")
    if hasattr(download_item, 'drive_file'):
        file = download_item.drive_file
        try:
            file_path = file.file.path
            filename = file.name
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read())
                    response['Content-Type'] = 'application/octet-stream'
                    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
                    return response
            else:
                return HttpResponse("File does not exist.")
        except:
            return HttpResponse(500)
    if hasattr(download_item, 'drive_folder'):
        folder = download_item.drive_folder
        response = make_tmp_archive(folder)
        if response is not None:
            return response
        else:
            return HttpResponse(status=500)

    return HttpResponse(status=500)

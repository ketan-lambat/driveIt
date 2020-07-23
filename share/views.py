from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from drive_data.models import Item
from registration.models import User
from .models import SharedItem


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

    return render(request, 'share/view.html', context={'shared': shared})


def download_file(request ,guid, item_id):
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
        return FileResponse(open(shared.item.drive_file.file.path, 'rb'))
    if hasattr(shared.item, 'drive_folder'):
        return redirect('folder_download', kwargs={'pk': shared.item.pk})
    return HttpResponse('Coming...')

import shutil
import os
from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import HttpResponse


def make_tmp_archive(folder):
    static_folder = settings.MEDIA_ROOT

    upload_path = os.path.join(static_folder, "uploads")
    tmp_dir_path = os.path.join(upload_path, folder.name)

    if os.path.exists(tmp_dir_path):
        try:
            shutil.rmtree(tmp_dir_path)
        except OSError:
            return None

    if recursive_file_copy(upload_path, folder):
        try:
            path_zip = shutil.make_archive(tmp_dir_path, "zip", tmp_dir_path)
            response = HttpResponse(FileWrapper(open(path_zip, 'rb')), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{folder.name.replace(" ", "_")}.zip"'
            shutil.rmtree(tmp_dir_path)
            return response
        except OSError:
            return None
    else:
        return None


def recursive_file_copy(folder_name, folder):
    path = os.path.join(folder_name, folder.name)
    try:
        os.mkdir(path)
    except OSError:
        return None

    files = folder.files.all()
    for file in files:
        try:
            shutil.copy(file.file.path, path)
        except OSError:
            return None

    file_folders = folder.files_folder.all()

    for file_folder in file_folders:
        if recursive_file_copy(path, file_folder) is None:
            return None

    return True

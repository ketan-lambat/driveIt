from django.urls import path, re_path
from drive_data import views

urlpatterns = [
    path('', views.DriveDataView.as_view(), name='drive_home'),
    re_path(r'^(?P<path>[-a-zA-Z0-9%/]*)/upload/$', views.file_upload_view, name='file_upload_view'),
    re_path(r'^(?P<path>[a-zA-Z0-9%/]*)/create_folder/$', views.create_folder_view, name='create_folder_view'),
    re_path(r'^(?P<path>[a-zA-Z0-9%/]*)/$', views.FolderDataView.as_view(), name='folder_data'),
]

urlpatterns2 = [
    path('', views.upload, name='upload'),
    path('file_list/', views.file_list, name='file_list'),
    path('upload_file/', views.upload_file, name="upload_file"),
    path('files/<int:pk>/', views.delete_book, name='delete_file'),

    path('class/file_list/', views.FileListView.as_view(), name="class_file_list"),
    path('class/upload_file/', views.UploadFileVIew.as_view(), name="class_upload_file"),
]

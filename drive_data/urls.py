from django.urls import path, re_path
from drive_data import views

urlpatterns = [
	path('', views.DriveDataView.as_view(), name='drive_home'),
	path('delete/<pk>/', views.file_delete_view, name="delete_file"),
	path('delete_folder/<pk>/', views.folder_delete_view, name="delete_folder"),

	# Make Sure to put regex path below other paths
	# otherwise re_path will consume the request
	# leading to a HTTP 405 Error or "Not Found" message
	re_path(r'^upload/(?P<path>[-a-zA-Z0-9%/]*)$', views.file_upload_view, name='file_upload_view'),
	re_path(r'^create_folder/(?P<path>[a-zA-Z0-9%/]*)$', views.create_folder_view, name='create_folder_view'),
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

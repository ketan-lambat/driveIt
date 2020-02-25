from django.urls import path
from drive_data import views

urlpatterns = [
	path('', views.upload, name='upload'),
	path('file_list/', views.file_list, name='file_list'),
	path('upload_file/', views.upload_file, name="upload_file"),
	path('files/<int:pk>/', views.delete_book, name='delete_file'),

	path('class/file_list/', views.FileListView.as_view(), name="class_file_list"),
	path('class/upload_file/', views.UploadFileVIew.as_view(), name="class_upload_file"),
]

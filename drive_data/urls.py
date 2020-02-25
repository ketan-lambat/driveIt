from django.urls import path
from drive_data import views

urlpatterns = [
	path('', views.upload, name='upload'),
	path('file_list/', views.file_list, name='file_list'),
	path('upload_file', views.upload_file, name="upload_file"),
]

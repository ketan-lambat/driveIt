from django.urls import path, re_path
from drive_data import views

urlpatterns = [
	path("", views.DriveDataView.as_view(), name="drive_home"),
	path("delete/<pk>/", views.file_delete_view, name="delete_file"),
	path("delete_folder/<pk>/", views.folder_delete_view, name="delete_folder"),
	# path("download/<path>", views.file_download_view, name="file_download"),
	path("download/", views.folder_download_view, name="folder_download"),
	# Make Sure to put regex path below other paths
	# otherwise re_path will consume the request
	# leading to a HTTP 405 Error or "Not Found" message
	re_path(
		r"^upload/(?P<path>[-a-zA-Z0-9%/]*)$",
		views.file_upload_view,
		name="file_upload_view",
	),
	re_path(
		r"^create_folder/(?P<path>[a-zA-Z0-9%/]*)$",
		views.create_folder_view,
		name="create_folder_view",
	),
	re_path(
		r"^(?P<path>[a-zA-Z0-9%/]*)/$",
		views.FolderDataView.as_view(),
		name="folder_data",
	),
	# re_path(
	# 	r"^download/(?P<path>[a-zA-Z0-9%/]*)$",
	# 	views.file_download_view,
	# 	name="file_download",
	# )
]

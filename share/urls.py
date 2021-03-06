from django.urls import path
from .views import share_item, shared_item_view, download_file, shared_folder_view

urlpatterns = [
    path('share/d/<item_id>', share_item, name='share_item'),
    path('share/f/<guid>', shared_item_view, name='shared_view'),
    path('download/<guid>/<item_id>', download_file, name='download_file'),
    path('view_share_folder/<guid>/<item_id>', shared_folder_view, name='share_folder_data')
]

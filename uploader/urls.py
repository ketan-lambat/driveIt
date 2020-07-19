from django.urls import re_path, include
from uploader.views import UploadViewSet
from uploader.routers import TusAPIRouter

router = TusAPIRouter()
router.register(r"files", UploadViewSet, basename="upload")

app_name = "uploads"

urlpatterns = [re_path(r"", include((router.urls, "uploads"), namespace="api"))]

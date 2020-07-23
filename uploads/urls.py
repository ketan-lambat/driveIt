from django.urls import re_path, include
from uploads.views import UploadViewSet
from uploads.routers import TusAPIRouter
from django.views.decorators.csrf import csrf_exempt

router = TusAPIRouter()
router.register(r"files", UploadViewSet, basename="upload")

app_name = "uploads"

urlpatterns = [re_path(r"", include((router.urls, "uploads"), namespace="api"))]

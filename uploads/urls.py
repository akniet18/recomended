from django.urls import path, include
from .views import UploadFileView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('uploads', UploadFileView)

urlpatterns = [
    # path('', UploadFileView.as_view(), name='uploads')
    path('', include(router.urls)),
]

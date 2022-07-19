from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import viewsets

from .serializers import UploadSerializer
from .models import Upload


# class UploadFileView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     parser_classes = (MultiPartParser, FormParser)
#     serializer_class = [UploadSerializer]
#     def post(self, request, *args, **kwargs):
#         file_serializer = UploadSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_serializer.save()
#             return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get_queryset(self):
#
#
#     def get(self, request, *args, **kwargs):
#         return Response({'ERR': 'GET METHOD NOT ALLOWED', 'STATUS': status.HTTP_405_METHOD_NOT_ALLOWED})


class UploadFileView(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer

    def pre_save(self, obj):
        obj.file = self.request.FILES.get('file')

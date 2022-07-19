import os
from rest_framework import serializers
from .models import Upload
# from review.serializers import ReviewSerializer
from uploads.utils import validate_file_size,validate_file_extension

class UploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True, validators=[validate_file_size, validate_file_extension])
    class Meta:
        model = Upload
        fields = ('id', 'name', 'uploaded_at', 'file')
        read_only_fields = ('id',)

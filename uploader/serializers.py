from django.urls import reverse
from rest_framework import serializers
from uploads.models import get_upload_model, Upload


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_upload_model()
        fields = '__all__'


class UploadSerializer2(serializers.ModelSerializer):
    upload_offset = serializers.IntegerField(label='Upload-Offset',
                                             read_only=True)
    upload_length = serializers.IntegerField(label='Upload-Length',
                                             read_only=True)
    upload_url = serializers.SerializerMethodField('get_upload_url',
                                                   read_only=True)

    class Meta:
        model = Upload
        fields = ['upload_offset', 'upload_length', 'filename', 'expires',
                  'upload_url']

    def get_upload_url(self, upload):
        if upload:
            return reverse('upload:api:upload-detail',
                           kwargs={'guid': upload.guid})
        else:
            return None

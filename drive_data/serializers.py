from django.urls import reverse
from drive_data.models import File
from rest_framework import serializers


class FileModelSerializer(serializers.ModelSerializer):
    upload_url = serializers.SerializerMethodField(source='get_upload_url',
                                                   read_only=True)
    file = serializers.FileField(read_only=True)

    class Meta:
        model = File
        fields = ['pk', 'name', 'file', 'file_size', 'upload_url']

    def get_upload_url(self, demo):
        if demo is not None and demo.file_id is not '':
            return reverse('uploads:api:upload-detail',
                           kwargs={'guid': demo.temp_file_id})
        else:
            return None

    def get_download_url(self, demo):
        request = self.context.get('request')
        if demo.file and hasattr(demo.file, 'url'):
            url = demo.file.url
            return request.build_absolute_uri(url)
        else:
            return None

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(FileModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

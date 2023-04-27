from rest_framework import serializers

from system.models import FileList
from system.utils.serializers import CustomModelSerializer


class SimpleFileSerializer(CustomModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
        return 'media/' + str(instance.url)

    class Meta:
        model = FileList
        fields = ('id', 'name', 'url')

    def create(self, validated_data):
        validated_data['name'] = str(self.initial_data.get('file'))
        validated_data['url'] = self.initial_data.get('file')
        return super().create(validated_data)


class FileSerializer(CustomModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
        return 'media/' + str(instance.url)

    class Meta:
        model = FileList
        fields = "__all__"

    def create(self, validated_data):
        validated_data['name'] = str(self.initial_data.get('file'))
        validated_data['url'] = self.initial_data.get('file')
        return super().create(validated_data)



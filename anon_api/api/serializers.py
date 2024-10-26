from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'original_image', 'anonymized_image', 'created_at', 'updated_at']
        read_only_fields = ['anonymized_image', 'created_at', 'updated_at']


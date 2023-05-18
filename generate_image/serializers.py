from rest_framework import serializers
from .models import GeneratedImage, Like
from django.conf import settings
class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedImage
        fields = ['id', 'image']
        
    def to_representation(self, instance):
        """
        Serialize image field to return url
        """
        ret = super().to_representation(instance)
        ret['image'] = self.context['request'].build_absolute_uri(ret['image'])
        return ret

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data['image'] = self.context['request'].build_absolute_uri(data['image'])
        return data


class SaveLikeSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['image', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and obj.image.image:
            media_url = request.build_absolute_uri(settings.MEDIA_URL)
            return media_url + str(obj.image.image)
        return None
  

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     ret['image'] = self.context['request'].build_absolute_uri(ret['image'])
    #     return ret
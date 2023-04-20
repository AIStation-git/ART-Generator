import os
import requests
from django.core.files.base import ContentFile
import io
from django.shortcuts import render
from .utils import generate_image
from rest_framework import generics
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import GalleryImageSerializer, LikeSerializer
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

# @csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
class GenerateImageView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(self.request.user, 'request')
        # Get the text input from the form
        text_input = request.POST.get('text_input')
        print(text_input, 'text______image')
        negative_input = request.POST.get('negative_input')
        num_images = int(request.POST.get('num_images', 1)) 
        style = request.POST.get('style')
        user = request.POST.get('user')

        
        # Generate the image using the util function
        user = User.objects.get(id=user)
        image_url = generate_image(text_input, negative_input, num_images, style, user=user, )


        # Return a JSON response with the image URL
        response_data = {'image_url': image_url}
        return JsonResponse(response_data)
    

class UpscaleImageView(View):
    def post(self, request, *args, **kwargs):
        engine_id = "esrgan-v1-x2plus"
        api_host = os.getenv('API_HOST')
        api_key = os.getenv('STABILITY_API_KEY')

        if api_key is None:
            return Response({"error": "Missing Stability API key."}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES.get("image")
        if image_file is None:
            return Response({"error": "Missing image file."}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "width": request.data.get("height", 1024),
            "height": request.data.get("height", None)  # Get the 'height' parameter from the request body
        }

        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/image-to-image/upscale",
            headers={
                "Accept": "image/png",
                "Authorization": f"Bearer {api_key}"
            },
            files={
                "image": image_file
            },
            data=data
        )

        if response.status_code != 200:
            return Response({"error": "Non-200 response from remote server."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save the upscaled image to a Django model
        upscaled_image = UpscaledImage()
        upscaled_image.image.save(f"upscaled_image_{request.user.pk}.png", ContentFile(response.content))

        return Response({"url": upscaled_image.image.url})

class GalleryImageListView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = GeneratedImage.objects.all()
    serializer_class = GalleryImageSerializer

    # def get_queryset(self):
    #     user = self.request.user
    #     return GeneratedImage.objects.filter(user=user)    


class LikeImageView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    def post(self, request, *args, **kwargs):
        image = get_object_or_404(GeneratedImage, id=self.kwargs['pk'])
        user = request.user
        
        # Check if the user has already liked the image
        if Like.objects.filter(user=user, image=image).exists():
            return Response({'error': 'You have already liked this image.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add a new like to the image
        like = Like.objects.create(user=user, image=image)
        like.save()
        
        return Response({'success': 'Image liked successfully.'}, status=status.HTTP_201_CREATED)
    

class DisplayLikeImageView(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

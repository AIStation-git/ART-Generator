from accounts.models import User
from .utils import generate_image
from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from django.views.generic import ListView
from django.http import HttpResponseBadRequest


import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


def generate_image_view(request):
    if request.method == 'POST':
        # Get the text input from the form
        text_input = request.POST.get('text_input')
        negative_input = request.POST.get('negative_input')
        num_images = int(request.POST.get('num_images', 1)) 
        style = request.POST.get('style')
         # default to 1 if not specified
        print(text_input, 'text______image')
        
        # Generate the image using the util function
        user = User.objects.get(email='raorehmat11@gmail.com')
        image_url = generate_image(text_input, negative_input, num_images, style, user=user, )

        return redirect('show_images')
        
        # return render(request, 'generated_image.html', {'image_url': image_url})

    else:
        # Render the form template if no form has been submitted
        return render(request, 'text_input_form.html')


class ImageListView(ListView):
    model = GeneratedImage
    template_name = 'image_list.html'
    context_object_name = 'images'

    # def get_queryset(self):
    #     qs = super().get_queryset()
        # if self.request.user.is_authenticated:
        #     qs = qs.filter(user=self.request.user)
        # else:
        #     qs = qs.none()
        # return qs  



def save_like(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        if not image_id:
            return HttpResponseBadRequest("Invalid request.")
        try:
            image = GeneratedImage.objects.get(id=image_id)
        except GeneratedImage.DoesNotExist:
            return HttpResponseBadRequest("Image not found.")
        user = User.objects.get(email='raorehmat11@gmail.com')
        like, created = Like.objects.get_or_create(user=user, image=image)
        if not created:
            # The like already exists
            pass
        return redirect('show_images')
    else:
        return HttpResponseBadRequest("Invalid request method.")


  

from django.conf import settings
from django.views import View
# class UpscaleView(View):
#     def get(self, request):
#         # Our Host URL should not be prepended with "https" nor should it have a trailing slash.
#         os.environ['STABILITY_HOST'] = 'https://api.stability.ai'

#         # Sign up for an account at the following link to get an API Key.
#         # https://dreamstudio.ai/

#         # Click on the following link once you have created an account to be taken to your API Key.
#         # https://dreamstudio.ai/account

#         # Paste your API Key below.

#         os.environ['STABILITY_KEY'] = 'sk-0R9i9jdidTSpAIKYEsQpv5Tv2Mvpc0GvFcS2xpgC8D5ay8sq'
#         # Set up our connection to the API.
#         stability_api = client.StabilityInference(
#             key=os.environ['STABILITY_KEY'], # API Key reference.
#             upscale_engine="esrgan-v1-x2plus", # The name of the upscaling model we want to use.
#             verbose=True, # Print debug messages.
#         )

#         # Import our local image to use as a reference for our upscaled image.
#         # img = Image.open('media/v1_txt2img_0.png')

#                 # Get the path to the image file in the media directory
#         # img_path = os.path.join(settings.MEDIA_ROOT, 'v1_txt2img_0.png')
#         img_path = os.path.join(os.path.dirname(__file__), 'test.jpeg')
#         # Open the image with PIL
#         img = Image.open(img_path)
#         print(img, 'img')

#         # Pass our image to the API and call the upscaling process.
#         answers = stability_api.upscale(init_image=img)
#         print(answers, 'answers')
        # upscaled_image = stability_api.upscale(init_image=img)

        # Set up our warning to print to the console if the adult content classifier is tripped.
# If adult content classifier is not tripped, save our image.

        # for resp in answers:
        #     for artifact in resp.artifacts:
        #         if artifact.finish_reason == generation.FILTER:
        #             warnings.warn(
        #                 "Your request activated the API's safety filters and could not be processed."
        #                 "Please submit a different image and try again.")
        #         if artifact.type == generation.ARTIFACT_IMAGE:
        #             big_img = Image.open(io.BytesIO(artifact.binary))
        #             big_img.save("imageupscaled" + ".png") # Save our image to a local file.

        # context = {'upscaled_image': answers}
        # return render(request, 'upscale.html', context)

import requests
from django.core.files.base import ContentFile
import io


engine_id = "esrgan-v1-x2plus"
api_host = os.getenv("API_HOST", "https://api.stability.ai")
api_key = os.getenv("STABILITY_API_KEY")

if api_key is None:
    raise Exception("Missing Stability API key.")

def upscale_image(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        width = request.POST.get('width', 1024)

        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/image-to-image/upscale",
            headers={
                "Accept": "image/png",
                "Authorization": f"Bearer {api_key}"
            },
            files={
                "image": image_file
            },
            data={
                "width": width,
            }
        )

        if response.status_code == 200:
            # Save the upscaled image to a file or variable
            upscaled_image = UpscaledImage()
            # upscaled_image = response.content
            upscaled_image.image.save(f"upscaled_image_{request.user.pk}.png", ContentFile(response.content))
            # Render the template with the upscaled image
            return render(request, 'upscale.html', {'upscaled_image': upscaled_image})
        else:
            # Handle the error case
            error_message = "Non-200 response: " + str(response.text)
            return render(request, 'upscale.html', {'error_message': error_message})
    else:
        # Render the empty form
        return render(request, 'upscale.html')
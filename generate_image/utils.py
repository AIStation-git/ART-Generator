import os
import requests
import base64
from django.core.files.base import ContentFile
from .models import GeneratedImage

def generate_image(text_input, num_images, style, user):
    # engine_id = "stable-diffusion-v1-5"
    engine_id = "stable-diffusion-xl-beta-v2-2-2"

    # engine_id="stable-diffusion-xl-beta-v2-2-2"
    api_host = os.getenv('API_HOST')
    # STABILITY_API_KEY = 'sk-73T7xGAhj5fG0NNUaPcO1BCbzQ434yICdSW1aV2w7TrdAggA'
    # api_key = STABILITY_API_KEY
    api_key = os.getenv('STABILITY_API_KEY')

    if api_key is None:
        raise Exception("Missing Stability API key.")

    payload = {
        "text_prompts": [
            {
                "text": text_input,
                "class": "pos"  # positive prompt
            },
        #       {
        #     "text": negative_input,
        #     "class": "neg"  # negative prompt
        # }
        ],
        "cfg_scale": 7,
        "clip_guidance_preset": "FAST_BLUE",
        "height": 512,
        "width": 512,
        "samples": num_images,
        "steps": 30,
        # 'style':style,
        "style_preset": style,  # use the "Anime Style"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    # Save the generated image to a Django model
    # for i, image in enumerate(data["artifacts"]):
    #     image_data = base64.b64decode(image["base64"])
    #     file_name = f"v1_txt2img_{i}.png"
    #     generated_image = GeneratedImage(text_input=text_input, negative_prompt='negative_input', style=style, number_of_images=num_images,  user=user)
    #     generated_image.image.save(file_name, ContentFile(image_data), save=True)

    # # Get the URL of the generated image
    # image_url = generated_image.image.url

    image_urls = []
    for i, image in enumerate(data["artifacts"]):
        image_data = base64.b64decode(image["base64"])
        file_name = f"v1_txt2img_{i}.png"
        generated_image = GeneratedImage(text_input=text_input, negative_prompt='negative_input', style=style, number_of_images=num_images,  user=user)
        generated_image.image.save(file_name, ContentFile(image_data), save=True)
        image_url = generated_image.image.url
        image_urls.append(image_url)
    print(image_urls, 'urls____')
    return image_urls


    # # Add the positive prompt if it was filled out by the user
    # if text_input:
    #     text_prompts.append({
    #         "text": text_input,
    #         "class": "pos"  # positive prompt
    #     })

    # # Add the negative prompt if it was filled out by the user
    # if negative_input:
    #     text_prompts.append({
    #         "text": negative_input,
    #         "class": "neg"  # negative prompt
    #     })

    # # Make sure at least one prompt was provided
    # if not text_prompts:
    #     raise Exception("At least one prompt is required.")
# Anime
# Line art
# Photographic
# Digital art
# Comic book
# Pixel art
# 3D model
# Cinematic
# Craft
# Clay
# Low poly
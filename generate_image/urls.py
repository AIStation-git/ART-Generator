from django.urls import path
from .views import GenerateImageView, GalleryImageListView, LikeImageView, DisplayLikeImageView, UpscaleImageView
#for dashboard
from .dashboard_view import save_like, ImageListView, generate_image_view, upscale_image

urlpatterns = [
    path('generate/images/', GenerateImageView.as_view(), name='generate_image'),
    #Gallery Image
    path('gallery/images/', GalleryImageListView.as_view(), name='gallery_image'),
    #like api
    path('images/like/', LikeImageView.as_view(), name='like_image'),
    path('list/like/images/', DisplayLikeImageView.as_view(), name='list_like_image'),

    #upscale image
    path('upscale/images/', UpscaleImageView.as_view(), name='upscale_image'),




    

    #Dashboard
    path('generate_image/', generate_image_view, name='generate_image'),
    #show images
    path('show/images/', ImageListView.as_view(), name='show_images'),
    #like image
    path('like/', save_like, name='save_like'),
    #upscale
    path('upscale/', upscale_image, name='upscale_image'),

]
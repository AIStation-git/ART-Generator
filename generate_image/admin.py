from django.contrib import admin
from .models import GeneratedImage, Like, UpscaledImage
# Register your models here.
@admin.register(GeneratedImage)
class GeneratedImageAdmin(admin.ModelAdmin):
    list_display = ('text_input', 'image')
    list_filter = ('text_input',)
    search_fields = ('text_input',)

admin.site.register(Like)
admin.site.register(UpscaledImage)



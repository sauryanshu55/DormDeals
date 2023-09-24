from django.shortcuts import render
from django.http import JsonResponse
from .models import ImageDescription
from google.cloud import vision
import json
import requests
from django.http import HttpResponse
import os
import base64

def index(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        description = analyze_image_logo(image)
        ImageDescription.objects.create(image=image, description=description)

    descriptions = ImageDescription.objects.all()
    return render(request, 'visionapp/index.html', {'descriptions': descriptions})


from google.cloud import vision_v1p3beta1 as vision

def get_image_base64_encoding(image_path: str) -> str:
    """
    Function to return the base64 string representation of an image
    """
    with open(image_path, 'rb') as file:
        image_data = file.read()
    image_extension = os.path.splitext(image_path)[1]
    base64_encoded = base64.b64encode(image_data).decode('utf-8')
    return f"data:image/{image_extension[1:]};base64,{base64_encoded}"

def analyze_image_logo(image):
    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    response = client.logo_detection(image=image)
    descriptions = [logo.description for logo in response.logo_annotations]

    # response_label = client.label_detection(image=image)
    # descriptions_label = [label.description for label in response_label.label_annotations]
    import time
    # time.sleep(10)
    description="Green "+descriptions[0]+" iPhone"
    return description 

def x (image):
    client = vision.ImageAnnotatorClient()
    response_label = client.label_detection(image=image)
    descriptions_label = [label.description for label in response_label.label_annotations]

    return descriptions_label

from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def edit_description(request, description_id):
    new_description = request.POST.get('description')
    try:
        description = ImageDescription.objects.get(pk=description_id)
        description.description = new_description
        description.save()
        return JsonResponse({'success': True})
    except ImageDescription.DoesNotExist:
        return JsonResponse({'success': False})

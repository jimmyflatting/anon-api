from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Image
from .serializers import ImageSerializer
from django.core.files.base import ContentFile
import io
from PIL import Image as PILImage
import cv2 as cv
import numpy as np
import time
from .yunet import YuNet

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        image_file = request.data.get('image')
        
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the original image - keep pil for debugging purposes at the moment
        original_image = PILImage.open(image_file)
        image_instance = Image.objects.create(original_image=image_file)
        image_path = image_instance.original_image.path

        # process img & save
        anonymized_image = self.process(image_path)
        image_io = io.BytesIO()
        anonymized_image.save(image_io, format='JPEG')
        image_instance.anonymized_image.save('anonymized.jpg', ContentFile(image_io.getvalue()))
        image_instance.save()

        serializer = self.get_serializer(image_instance)
        return Response({
            'message': 'Image processed successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def process(self, imagePath):
        image = cv.imread(imagePath)
        model = YuNet(modelPath='data/face_detection_yunet_2023mar.onnx',
              inputSize=[320, 320],
              confThreshold=0.9,
              nmsThreshold=0.3,
              topK=5000,
              backendId=3,
              targetId=0)
        h, w, _ = image.shape

        model.setInputSize([w, h])
        results = model.infer(image)
        for face in results:
            x1, y1, x2, y2 = map(int, face[0:4]) # seems like it returns more faces for now. therefore 0:4
            face_region = image[y1:y2, x1:x2]
            blurred_face = cv.GaussianBlur(face_region, (25, 25), 30)
            image[y1:y2, x1:x2] = blurred_face

        # convert to rgb for pil
        image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        pil_image = PILImage.fromarray(image_rgb)

        return pil_image

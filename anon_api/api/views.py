from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Image
from .serializers import ImageSerializer
from django.core.files.base import ContentFile
import io
from PIL import Image as PILImage
from PIL import Image, ImageFilter
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

        # Process and anonymize the image
        original_image = PILImage.open(image_file)
        anonymized_image = self.process(original_image)

        # Save the anonymized image
        image_io = io.BytesIO()
        anonymized_image.save(image_io, format='JPEG')

        # Create the Image instance
        image = Image.objects.create(
            original_image=image_file,
            anonymized_image=ContentFile(image_io.getvalue(), name='anonymized.jpg')
        )

        serializer = self.get_serializer(image)
        return Response({
            'message': 'Image processed successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def process(self):
        self.image = cv.imread(self.image)
        self.k = 100
        self.model = YuNet(modelPath='data/face_detection_yunet_2023mar.onnx',
              inputSize=[320, 320],
              confThreshold=0.9,
              nmsThreshold=0.3,
              topK=5000,
              backendId=3,
              targetId=0)
        self.h, self.w, _ = self.image.shape

        self.model.setInputSize([self.w, self.h])
        tic = time.perf_counter()
        for i in range(1, self.k):
            results = self.model.infer(self.image)
            # blur faces
            for face in results:
                x1, y1, x2, y2, _ = face
                self.image[y1:y2, x1:x2] = cv.GaussianBlur(self.image[y1:y2, x1:x2], (99, 99), 30)
        toc = time.perf_counter()

        return self.image
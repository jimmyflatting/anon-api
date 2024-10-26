from django.test import TestCase
from .models import Image
from .views import ImageViewSet

# Create your tests here.
class ImageTestCase(TestCase):
    def test_image_upload(self):
        Image.objects.create(original_image="media/original_images/59jnia4h74za1.jpg", anonymized_image="media/anonymized_images/59jnia4h74za1.jpg")
        image = Image.objects.get(original_image="media/original_images/59jnia4h74za1.jpg")
        self.assertEqual(image.original_image, "media/original_images/59jnia4h74za1.jpg")
        self.assertEqual(image.anonymized_image, "media/anonymized_images/59jnia4h74za1.jpg")
    
    def test_image_delete(self):
        image = Image.objects.get(original_image="media/original_images/59jnia4h74za1.jpg")
        image.delete()
        with self.assertRaises(Image.DoesNotExist):
            Image.objects.get(original_image="media/original_images/59jnia4h74za1.jpg")
    
    def test_image_process(self):
        image = Image.objects.get(original_image="media/original_images/59jnia4h74za1.jpg")
        blur = ImageViewSet().process()
        self.assertEqual(blur, "media/anonymized_images/59jnia4h74za1.jpg")

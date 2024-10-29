import cv2 as cv
import cv2.data as data

class ImageProcessor:
    def __init__(self, image_path, border = True):
        self.image = cv.imread(image_path)
        self.border = border
        self.height, self.width, self.channels = self.image.shape

    def process(self):
        grayscale = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        
        face_classifier = cv.CascadeClassifier(
            data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        face = face_classifier.detectMultiScale(
            grayscale, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
        )

        for (x, y, w, h) in face:
            if self.border:
                cv.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 4)
            face_region = self.image[y:y+h, x:x+w]
            blurred_face = cv.GaussianBlur(face_region, (25, 25), 40)
            self.image[y:y+h, x:x+w] = blurred_face
        
        return cv.cvtColor(self.image, cv.COLOR_BGR2RGB)

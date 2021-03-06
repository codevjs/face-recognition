import cv2
import os
import numpy
import pickle
from PIL import Image

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
image_dir     = os.path.join(BASE_DIR, "images")

face_casecade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer    = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids  = {}
y_labels   = []
x_train    = []

for root, dirs, files in os.walk(image_dir):
    for file in files:

        if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
            path  = os.path.join(root, file)
            label = os.path.basename(os.path.dirname(path)).replace("-", " ").lower()

            if label in label_ids:
                pass
            else:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]

            # y_labels.append(label) # some number
            # x_train.append(path)   # verify this image, turn to a NUMPY array, GRAY
            pil_image   = Image.open(path).convert("L") #greyscale
            size        = (550, 550)
            final_image  = pil_image.resize(size, Image.ANTIALIAS)
            image_array = numpy.array(pil_image, "uint8")
            faces = face_casecade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

            for (x,y,w,h) in faces:
                roi = image_array[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)

# print(y_labels)
# print(x_train)

with open("labels.pickle", "wb") as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, numpy.array(y_labels))
recognizer.save("trainner.yml")
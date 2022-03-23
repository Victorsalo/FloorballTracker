# Identifiering av spelaren
import cv2
import keras
import os
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

# introducera minsta sannolikhet för att eliminera svaga förutsägelser
p_min = 0.5
thres = 0.

# 'VideoCapture' object and reading vicv2.mean(image, mask=mask)deo from a file
video = cv2.VideoCapture('namnpavideon')
writer = None
h, w = None, None

# # Skapa labels i listan
with open('coco.names') as f:
    labels = [line.strip() for line in f]

# nu ska man loada nätverket
network = cv2.dnn.readNet('darknet/cfg/yolov3.weights', 'darknet/cfg/yolov3.cfg')

# Få fram output layer names som vi behöver från YOLO
ln = network.getLayerNames()
ln = [ln[i[0] - 1] for i in network.getUnconnectedOutLayers()]

# Defina loop som fångar framsen
while True:
    ret, frame = video.read()
    if not ret:
        break
    # frame preprocessing
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    # perform a forward pass of the YOLO object detector, vilket ger oss våra begränsningsrutor och tillhörande sannolikheter.
    network.setInput(blob)
    outputfromnetwork = network.forward(ln)

# -------------------------------------------------------------------
# Detektering av nummer

# ladda VGG16 nätverket
vgg = VGG16(weights="imagenet", include_top=False, input_tensor=Input(shape=(koordinater, koordinater, koordinater)))


# flatten the max-pooling output of VGG
flatten = vgg.output
flatten = Flatten()(flatten)
# construct a fully-connected layer header to output the predicted bounding box coordinates
boundingboxHead = Dense(koordinater, activation="relu")(flatten)
boundingboxHead = Dense(koordinater, activation="relu")(boundingboxHead)

# sen skapar man modellen
model = Model(inputs=vgg.input, outputs=boundingboxHead)

# ----------------------------------------------------------------------
# Identifiering av nummer

classifier = Sequential()
classifier.add(Conv2D(128, (3, 3), input_shape=(224, 224, 3), activation='relu'))
classifier.add(MaxPool2D(pool_size=(2, 2)))
classifier.add(Dropout(0.2))
classifier.add(Conv2D(64, (3, 3), activation='relu'))
classifier.add(MaxPool2D(pool_size=(2, 2)))
classifier.add(Dropout(0.2))
classifier.add(Conv2D(32, (3, 3), activation='relu'))
classifier.add(MaxPool2D(pool_size=(2, 2)))
classifier.add(Dropout(0.2))
classifier.add(Flatten())
classifier.add(Dense(units=128, activation='relu'))
classifier.add(Dense(units=64, activation='relu'))
classifier.add(Dense(units=64, activation='relu'))
classifier.add(Dense(units=10, activation='softmax'))
# Compiling the CNN
classifier.compile(optimizer='namn', loss='crossentropy', metrics=['accuracy'])

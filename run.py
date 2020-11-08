import cv2 as cv
import os
import argparse 
import itertools

def accumulate(I):
    it = itertools.groupby(I, operator.itemgetter(0))
    for key, subiter in it:
        yield key, sum(item[1] for item in subiter)


labelsPath = os.path.sep.join(["pretrained",
	"object_detection_classes_coco.txt"])
LABELS = open(labelsPath).read().strip().split("\n")

color = (255,0,0)
 
img = cv.imread('input.jpg')
rows = img.shape[0]
cols = img.shape[1]

cvNet = cv.dnn.readNetFromTensorflow('./pretrained/frozen_inference_graph.pb', './pretrained/graph.pbtxt')
cvNet.setInput(cv.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))
cvOut = cvNet.forward()

all_obejcts = []

for detection in cvOut[0,0,:,:]:
    score = float(detection[2]) # same with float(detection[0,0,i,2])
    classID = int(detection[1]) # same with int(detection[0,0,i,1])

    if score > 0.3:
        left = detection[3] * cols
        top = detection[4] * rows
        right = detection[5] * cols
        bottom = detection[6] * rows

        text = "{}: {:.4f}".format(LABELS[classID], score)
        
        cv.putText(img, text, (int(left), int(top)-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)


        all_objects.append([classID, ])






# if you want to see the result
cv.imshow('img', img)
cv.waitKey()


# if __name__ == "__main__":
#     ap = argparse.ArgumentParser()
#     ap.add_argument("-i")


import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import os


def detect_car_person(img_name):
    im = cv2.imread(img_name)
    bbox, label, conf = cv.detect_common_objects(im)

    if(label.count('car') > 0 and label.count('person') ==0 ):
        return img_name
    else:
        return None





if __name__ == '__main__':

    print('scanning....')

    for (path, dir, files) in os.walk("./photos"):
        print('gogogo')
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.jpg':
                car_filtered = detect_car_person(path+'/'+filename)
                if(car_filtered is not None):
                    print(car_filtered)
    
    print('completed')
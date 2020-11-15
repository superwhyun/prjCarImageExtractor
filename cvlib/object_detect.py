import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import argparse
import os
import shutil

target_class = [
    "person","bicycle","car","motorcycle","airplane","bus","train","truck","boat",
    "traffic light","fire hydrant","stop sign","parking meter","bench","bird",
    "cat","dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack",
    "umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball",
    "kite","baseball bat","baseball glove","skateboard","surfboard","tennis racket",
    "bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple","sandwich",
    "orange","broccoli","carrot","hot dog","pizza","donut","cake","chair","couch",
    "potted plant","bed","dining table","toilet","tv","laptop","mouse","remote",
    "keyboard","cell phone","microwave","oven","toaster","sink","refrigerator","book",
    "clock","vase","scissors","teddy bear","hair drier","toothbrush"]

def find_target_image(img_name, target, occur, expt):
    im = cv2.imread(img_name)

    # gpu enable을 하려면, pip install이 아니라 cvlib 소스코드 컴파일을 해야 함.
    bbox, label, conf = cv.detect_common_objects(im, enable_gpu=False)
    

    print('{0} has {1} {2} and {3} {4}'.format(img_name, target, label.count(target), expt, label.count(expt)))
    
    if(label.count(target) >= occur and label.count(expt) ==0 ):
        print('\t => this image needs to be moved')
        return img_name
    else:
        return None



if __name__ == '__main__':

    print('scanning....')

    ap = argparse.ArgumentParser(description='가비지 이미지 솎아내기')

    ap.add_argument('-i', '--input', type=str, default='./input', required=True, help='입력 디렉토리' )
    ap.add_argument('-o', '--output', type=str, default='./output', required=True, help='이동대상 디렉토리' )
    ap.add_argument('-t', '--target', type=str, required=True, help='이동 대상 객체 종류(e.g, car, person,...)')
    ap.add_argument('-m', '--min', type=int, default=1, required=False, help='이동 조건. target 객체의 출현 회수가 일정 개수 이상이면 이동대상임')
    ap.add_argument('-e', '--expt', required=False, help='이동 대상 객체 종류(e.g, car, person,...)')

    args = ap.parse_args()
    print('> input direcotry :\t', args.input)
    print('> output direcotry :\t', args.output)
    print('> target class :\t', args.target)
    print('> minimum occurrence :\t', args.min)
    print('> exception class :\t', args.expt)
    
    if(os.path.isdir(args.output)==False):
        os.mkdir(args.output)

    for (path, dir, files) in os.walk(args.input):
        print('gogogo')
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.jpg' or ext == '.png':
                filtered = find_target_image(path+'/'+filename, args.target, args.min, args.expt)
                if(filtered is not None):
                    shutil.move(filtered, args.output)
                    # shutil.copy2(filtered, args.output) # 메타속성 포함하여 복사하고자 할 경우
                    # print(filtered)
                else:
                    print('\tpass')
                
    
    print('completed')
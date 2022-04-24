import os
import subprocess
import sys
import shlex
import cv2 as cv
import shutil
import cameradetection


OUTPUT_DIR = os.path.join(cameradetection.ROOT_DIR, "people")
FRAMES_DIR = os.path.join(OUTPUT_DIR, "frames")
IMG_DIR = os.path.join(OUTPUT_DIR, "imgs")


def run(videopath, tool=None, timestamps=None):
    if tool is None:
        tool = os.path.join(cameradetection.ROOT_DIR, "Yolov5_DeepSort_Pytorch")
        tool = os.path.join(tool, "yolov5")
        tool = os.path.join(tool, "detect.py")
    createdirs()
    if len(os.listdir(FRAMES_DIR)) == 0:
        cropandcut(videopath, FRAMES_DIR)
    process = f"python {tool} --source {FRAMES_DIR} --save-crop --nosave \
                --classes 0 --project {OUTPUT_DIR} --name run"
    subprocess.run(shlex.split(process), check=True)
    shutil.rmtree(FRAMES_DIR)


def cropandcut(videopath, savedir):
    video = cv.VideoCapture(videopath)
    _, frame = video.read()
    roi = cameradetection.setupROI(frame)
    video.release()
    xstart, ystart, width, hight = roi[0], roi[1], roi[2], roi[3]
    filedest = os.path.join(savedir, "out%03d.png")
    process = f"ffmpeg -i {videopath} -filter:v \
              'crop={width}:{hight}:{xstart}:{ystart}, fps=1' {filedest}"
    subprocess.run(shlex.split(process), check=True)


def createdirs():
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    if not os.path.exists(FRAMES_DIR):
        os.mkdir(FRAMES_DIR)

if __name__ == "__main__":
    run(sys.argv[1])

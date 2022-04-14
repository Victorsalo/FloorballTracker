import os
import subprocess
import sys
import cameradetection
import shlex


def run(videopath, tool="../Yolov5_DeepSort_Pytorch/yolov5/detect.py", timestamps=None):
    OUTPUT_DIR = os.path.join(cameradetection.ROOT_DIR, "people")
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    if timestamps:
        cameradetection.cut_ffmpeg(videopath, timestamps)
    else:
        cameradetection.crop_ffmpeg(videopath, output=OUTPUT_DIR)
    IMG_DIR = os.path.join(OUTPUT_DIR, "imgs")
    if not os.path.exists(IMG_DIR):
        os.mkdir(IMG_DIR)
    command = f"python3 {tool} "
    subprocess.run(shlex.split(command))
    # Do yolo and save txt in outputdir, take txt and use opencv to extract all
    # the people for every frame


if __name__ == "__main__":
    run(sys.argv[1])

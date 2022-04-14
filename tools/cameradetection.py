"""
A module to see when a floorball clock is stopped.
In its first version it is to be used on two images and compare them.
In its second version it is to be used on a video file.
"""
import subprocess
import os
import math
import shlex
import shutil
import cv2 as cv
from sys import argv

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(ROOT_DIR, "tmp")
CROP_DIR = os.path.join(TMP_DIR, "crop")
CUT_DIR = os.path.join(TMP_DIR, "cut")
RESULT_DIR = os.path.join(TMP_DIR, "results")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")


def find_difference(img1, img2, roi):
    """
    Main function of cameradetection.
    Blurs images to remove noise, then a low threshold together with opening
    morphological operation removes any small changes.
    @returns True if clock is still going, False otherwise.
    @param image1 is the first image of the clock.
    @param image2 is the second image of the clock,
    with a time offset of slightly more than 1/fps relative to image1.
    """
    img1roi = extractROI(img1, roi)
    img2roi = extractROI(img2, roi)
    gray1 = cv.cvtColor(img1roi, cv.COLOR_BGR2GRAY)
    gray2 = cv.cvtColor(img2roi, cv.COLOR_BGR2GRAY)
    gray1blur = cv.GaussianBlur(gray1, (5, 5), 0)
    gray2blur = cv.GaussianBlur(gray2, (5, 5), 0)
    diff = cv.absdiff(gray1blur, gray2blur)
    # diffblur = cv.GaussianBlur(diff, (5, 5), 0)
    _, thresh = cv.threshold(diff, 30, 255, cv.THRESH_BINARY)
    element = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
    denoised_thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, element)
    # This number should be calculated based on the size of the roi.
    difference_threshold = 20
    return cv.countNonZero(denoised_thresh) > difference_threshold


def setupROI(img):
    img_resize = cv.resize(img, (1280, 720), cv.INTER_LINEAR)
    roi = cv.selectROI("Select ROI", img_resize, False)
    cv.destroyWindow("Select ROI")
    xscale = img.shape[0]/img_resize.shape[0]
    yscale = img.shape[1]/img_resize.shape[1]
    new_roi = [0]*4
    new_roi[0::2] = [math.floor(x*xscale) for x in roi[0::2]]
    new_roi[1::2] = [math.floor(y*yscale) for y in roi[1::2]]
    return new_roi


def extractROI(img, roi):
    return img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]


def from_images(img_path1, img_path2):
    """
    Plan: Take in video. Compare frames with 1/(fps*1.2) timestep.
    If same, add timestamp to list.
    Maybe cut the video when done. Might not need to.
    """
    img1 = cv.imread(img_path1)
    img2 = cv.imread(img_path2)
    roi = setupROI(img1)
    find_difference(img1, img2, roi)


def from_video(videopath):
    video = cv.VideoCapture(videopath)
    if not video.isOpened():
        print("Video can not be loaded")
        # Replace with exception and try again clause in caller.
        exit()
    success, frame = video.read()
    roi = setupROI(frame)
    timestamps = []
    running = False
    while True:
        success, frame1 = video.read()
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        time = video.get(cv.CAP_PROP_POS_MSEC)
        video.set(cv.CAP_PROP_POS_MSEC, time + 1200)
        success, frame2 = video.read()
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        diffrent = find_difference(frame1, frame2, roi)
        if diffrent != running:
            running = not running
            if running:
                timestamps.append([video.get(cv.CAP_PROP_POS_MSEC)])
            else:
                timestamps[-1].append(video.get(cv.CAP_PROP_POS_MSEC))
    video.release()
    return timestamps


# Takes about 9.5 minutes to crop 1 hour.
def crop_play_area(videopath):
    video = cv.VideoCapture(videopath)
    if not video.isOpened():
        print("Video can not be loaded")
        # Replace with exception and try again clause in caller.
        exit()
    success, frame = video.read()
    fps = video.get(cv.CAP_PROP_FPS)
    roi = setupROI(frame)
    # Replace this with function that finds regardless of corner started from.
    w = roi[2]
    h = roi[3]
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter('cropped.mp4', fourcc, fps, (w, h))
    # Timing stuff. Remove later.
    # frames = video.get(cv.CAP_PROP_FRAME_COUNT)
    # start = time.time()

    while True:
        success, frame = video.read()
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        crop_frame = extractROI(frame, roi)
        out.write(crop_frame)
    # Timing stuff.
    # stop = time.time()
    # print(f"Time per frame: {(stop - start)/frames}")

    video.release()
    out.release()


# Takes about 9 minutes to crop 1 hour.
def crop_ffmpeg(videopath, roi=None, order="", output=CROP_DIR):
    file_name, format = os.path.splitext(os.path.basename(videopath))
    if roi is None:
        video = cv.VideoCapture(videopath)
        if not video.isOpened():
            print("Video can not be loaded")
            # Replace with exception and try again clause in caller.
            exit()
        success, frame = video.read()
        roi = setupROI(frame)
    xstart = roi[0]
    ystart = roi[1]
    width = roi[2]
    hight = roi[3]
    part_name = os.path.join(output, file_name + order + format)
    process = f"ffmpeg -i {videopath} -filter:v 'crop={width}:{hight}:{xstart}:{ystart}' {part_name}"
    subprocess.call(shlex.split(process))
    return roi


def crop_from_dir(video_dir=CUT_DIR):
    parts = os.listdir(video_dir)
    parts_abs = [os.path.join(video_dir, part) for part in parts]
    roi = crop_ffmpeg(parts_abs[0])
    for part in parts_abs[1:]:
        order = "".join(filter(str.isdigit, part))
        crop_ffmpeg(part, roi, order)


def cut_ffmpeg(videopath, timestamps, output=CUT_DIR):
    """
    Maybe put things in a better folder
    """
    file_name, format = os.path.splitext(os.path.basename(videopath))
    timestamps = [[t[0]/1000, t[1]/1000] for t in timestamps]
    cnt = 0
    for interval in timestamps:
        part_name = os.path.join(output, file_name + str(cnt) + format)
        process = f"ffmpeg -ss {interval[0]} -i {videopath} -c copy -to {interval[1]} {part_name}"
        subprocess.run(shlex.split(process))
        cnt += 1


def create_dirs():
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)
    if not os.path.exists(CUT_DIR):
        os.mkdir(CUT_DIR)
    if not os.path.exists(CROP_DIR):
        os.mkdir(CROP_DIR)
    if not os.path.exists(RESULT_DIR):
        os.mkdir(RESULT_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)


def remove_dirs():
    """
    TODO: Should remove the dirs, and their content, created by create_dirs().
    """
    shutil.rmtree(TMP_DIR)


def main(isvideo, paths):
    if isvideo:
        from_video(paths)
    elif not isvideo:
        from_images(paths[0], paths[1])


if __name__ == "__main__":
    if len(argv) > 1:
        from_video(argv[1])
    else:
        main(False, ["../images/clock1.png", "../images/clock2.png"])

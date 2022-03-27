import subprocess
import sys
import os
from os.path import join
import shlex
import cameradetection
import average


def run(videopath):
    # detect timestamps, works
    timestamps = cameradetection.from_video(videopath)
    # cut video, works but video looks a little weird.
    cameradetection.create_dirs()
    cameradetection.cut_ffmpeg(videopath, timestamps)
    # crop videos
    cameradetection.crop_from_dir(videopath)
    # detect players
    detect()
    # Add path for Yolov5_DeepSort_Pytorch to work
    # detect numbers and track players
    # transform points
    players = []  # placeholder
    # calculate values
    processed_players = average.process_all(players, 30)  # Add detection
    # write values to file
    average.write_to_file(processed_players)
    # upload values.
    # clean up
    cameradetection.remove_dirs()


def detect():
    orig_path = os.getcwd()
    track_dir = join(cameradetection.ROOT_DIR, "Yolov5_DeepSort_Pytorch")
    os.chdir(track_dir)
    for part in os.listdir(cameradetection.CROP_DIR):
        abs_path_part = join(cameradetection.CROP_DIR, part)
        # Send to recocnition program
        track_tool = join(track_dir, "track.py")
        command = (
                f"python3 {track_tool} --source {abs_path_part} "
                "--yolo_model yolov5n.pt --classes 0 --save-txt "
                f"--project {cameradetection.RESULT_DIR} "
                "--name test"
                )
        subprocess.run(shlex.split(command))
    os.chdir(orig_path)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print("Incorrect input. Please give path of video")

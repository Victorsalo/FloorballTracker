import sys
import os
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
    for part in os.listdir(cameradetection.CROP_DIR):
        abs_path_part = os.path.join(cameradetection.CROP_DIR, part)
        # Send to recocnition program
        pass
    # detect numbers and track players
    # transform points
    # calculate values
    # write values to file
    # upload values.
    # clean up
    pass


if __name__ == "__main__":
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print("Incorrect input. Please give path of video")

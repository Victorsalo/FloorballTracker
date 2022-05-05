import subprocess
import sys
import os
from os.path import join
import shlex
import cameradetection
import average
import boundingtoposition
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore


def run(videopath, camera_calibration_matrix, detect=True, cleanup=True):
    if detect:
        # detect timestamps, works
        timestamps = cameradetection.from_video(videopath)
        print("timestamps done")
        # cut video, works but video looks a little weird.
        cameradetection.create_dirs()
        print("created dirs")
        cameradetection.cut_ffmpeg(videopath, timestamps)
        print("cut video")
        # crop videos
        cameradetection.crop_from_dir()
        print("cropped video")
        # detect players
        detection()
        print("detected players")
    # detect numbers and track players
    # transform points
    all_players = transform(camera_calibration_matrix, videopath)
    # calculate values
    processed_players = average.process_all(all_players, 30)  # Add detection
    print("processed players")
    # write values to file
    average.write_to_file(processed_players, cameradetection.OUTPUT_DIR)
    print("wrote to file")
    # upload values.
    if cleanup:
        # clean up
        cameradetection.remove_dirs()
        print("removed dirs")


def transform(camera_calibration_matrix, videopath):
    all_players = []
    calibration_points = boundingtoposition.setup(videopath)
    for subdir in os.listdir(cameradetection.RESULT_DIR):
        subdir_abs = os.path.join(cameradetection.RESULT_DIR, subdir)
        for part in os.listdir(subdir_abs):
            part_abs = os.path.join(subdir_abs, part)
            players = boundingtoposition.projection(part_abs,
                                                    camera_calibration_matrix,
                                                    calibration_points)
            for player in players:
                all_players.append(player)
    print("transformed points")
    return all_players


def detection():
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
                "--name test --exist-ok"
                )
        subprocess.run(shlex.split(command))
    os.chdir(orig_path)


def send_to_firebase(processed_players, cert):
    cred = credentials.Certificate(cert)
    app = firebase_admin.initialize_app(cred)
    store = firestore.client()
# [[playernumber, [[frame,], [x,], [y,], [speed,], [acceleration,]]],]
    labels = ["frame", "x", "y", "speed", "acceleration"]
    collection_list = store.collections()
    idcols = [int(col.id[5:]) for col in collection_list if col.id.startswith("Match")]
    if len(idcols) == 0:
        new_col_number = 0
    else:
        new_col_number = idcols.sort()[-1]+1
    collection_name = f"Match{new_col_number}"
    collection = store.collection(collection_name)
    for datapoints in processed_players:
        data = {}
        name = str(datapoints[0])
        for i in range(len(labels)):
            data[labels[i]] = datapoints[1][i]
        collection.document(name).set(data)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        run(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[3] == "--nodetect":
        run(sys.argv[1], sys.argv[2], detect=False)
    elif len(sys.argv) == 4 and sys.argv[3] == "--nocleanup":
        run(sys.argv[1], sys.argv[2], cleanup=False)
    elif len(sys.argv) == 5 and sys.argv[3] == "--nodetect" and sys.argv[4] == "--nocleanup":
        run(sys.argv[1], sys.argv[2], detect=False, cleanup=False)
    elif len(sys.argv) == 5 and sys.argv[4] == "--nodetect" and sys.argv[3] == "--nocleanup":
        run(sys.argv[1], sys.argv[2], detect=False, cleanup=False)
    else:
        print("Incorrect input. Please give path of video")

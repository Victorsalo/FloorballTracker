import numpy as np
import cv2
import yaml
import pandas
import calCordinates
# Punkter i planet för att calibrera homografi
import average
def setup(videopath):
    points1 = np.array([(0, 0), (4, 0), (4, 5), (0, 5)])
    points1 = np.float32(points1[:, np.newaxis, :])

    # Punkter i videon för att hitta homografi
    points2 = np.array(calCordinates.calCordinates(videopath))
    points2 = np.float32(points2[:, np.newaxis, :])
    return points2


#kalibreringsfil för kameran.
def read_calibration_matrix(calibration_matrix_yaml):
    a_yaml_file = open(calibration_matrix_yaml)
    parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

    newcameramtx = parsed_yaml_file["newcameramatrix"]
    newcameramtx = np.array(newcameramtx)


    mtx = parsed_yaml_file["camera_matrix"]
    mtx = np.array(mtx)

    dist = parsed_yaml_file["dist_coeff"]
    dist = np.array(dist)
    return newcameramtx, mtx, dist

def undistort(videopath, calibration_matrix_yaml, output_name):
    cap = cv2.VideoCapture(videopath)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    writer = cv2.VideoWriter(output_name, fourcc, fps, (width, height))
    newcameramtx, mtx, dist = read_calibration_matrix(calibration_matrix_yaml)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        writer.write(frame)
    cap.release()
    writer.release()
    


def find_homography(points2, calibration_matrix_yaml):
    points1 = np.array([(0, 0), (4, 0), (4, 5), (0, 5)])
    newcameramtx, mtx, dist = read_calibration_matrix(calibration_matrix_yaml)
    # Undistort punkterna som används för att hitta homografi. Koregerar för fisheye
    dstttt = cv2.undistortPoints(points2, mtx, dist, None, newcameramtx)
    homographymatrix, status = cv2.findHomography(dstttt, points1)
    return homographymatrix, dstttt



def Read(bounding_box_txt):
    X = open(bounding_box_txt, 'r')
    BusData = X.read()

    BusDataList = BusData.split()
    BusDataArray = np.array(BusDataList)
    num_lines = sum(1 for line in open(bounding_box_txt))
    BusDataReshaped = BusDataArray.reshape(num_lines, 10)  # Make a matrix out of 1D Array
    BusDataFrame = pandas.DataFrame(BusDataReshaped, columns=['f', 'id', 'x', 'y', 'w', 'h', 'u1', 'u2', 'u3', 'u4'])
    return BusDataFrame

def projection(bounding_box_txt, calibration_matrix_yaml, points2 ):
    newcameramtx, mtx, dist = read_calibration_matrix(calibration_matrix_yaml)
    homographymatrix, dsttt = find_homography(points2, calibration_matrix_yaml)

    BusDataFrame = Read(bounding_box_txt)

    numberOfId = 0
    for j in range(sum(1 for line in open(bounding_box_txt))):
        if int(BusDataFrame.id[j]) > numberOfId:
            numberOfId = int(BusDataFrame.id[j])

    playerData = []
    for i in range(numberOfId):
        cordinates = []
        individualPlayerData = []
        frames = []
        for j in range(sum(1 for line in open(bounding_box_txt))):
            if int(BusDataFrame.id[j]) == i + 1 :
                cordinates.append((int(BusDataFrame.x[j]) + (int(BusDataFrame.w[j]) / 2), int(BusDataFrame.y[j]) + int(BusDataFrame.h[j])))
                frames.append(int(BusDataFrame.f[j]))
                #print(cordinates)

        points = np.array(cordinates)
        #print(points)
        undistortedPointArrayZ1 = np.zeros((3, points.shape[0]))
        if points.size != 0:
            #print(cordinates)
            #points = np.array(cordinates)
            #print(points.shape[0])
            points = np.float32(points[:, np.newaxis, :])
            undistortedPoint = cv2.undistortPoints(points, mtx, dist, None, newcameramtx)

            #undistortedPointArray = []

            for k in range(points.shape[0]):
                undistortedPointArray = undistortedPoint[k][0]

                undistortedPointArrayZ1[0][k] = undistortedPointArray[0]
                undistortedPointArrayZ1[1][k]  = undistortedPointArray[1]
                undistortedPointArrayZ1[2][k] = 1


            x = np.dot(homographymatrix, undistortedPointArrayZ1)
            xDataMetric = []
            yDataMetric = []
            zDataMetric = []



            for k in range(points.shape[0]):

                xDataMetric.append(x[0][k] / x[2][k])
                yDataMetric.append(x[1][k] / x[2][k])
                zDataMetric.append(x[2][k] / x[2][k])


            individualPlayerData = [i+1, [frames, xDataMetric, yDataMetric]]

            playerData.append(individualPlayerData)





    return playerData

# playerData = projection("gear360FisheyeKarhall.txt", "calibration_matrix.yaml")
# playerData = average.process_all(playerData, 60)
# playerData = average.round_data(playerData)
# average.write_to_file(playerData)
# done

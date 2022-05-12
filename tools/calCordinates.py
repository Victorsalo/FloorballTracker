import cv2


def click_event(event, x, y, flags, params):

    bild = params[0]
    coordinates = params[1]
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        coordinates.append((x, y))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(bild, str(x) + ',' + str(y), (x, y), font, 1, (255, 0, 0), 2)
        cv2.imshow('img', bild)
    if event == cv2.EVENT_RBUTTONDOWN:
        print(x, ' ', y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        g = bild[y, x, 0]
        k = bild[y, x, 1]
        l = bild[y, x, 2]
        cv2.putText(bild, str(g) + ',' + str(k) + ',' + str(l), (x, y), font, 1, (255, 255, 0), 2)
        cv2.imshow('img', bild)

def calCordinates(videopath):
    vidcap = cv2.VideoCapture(videopath)
    funkar, img = vidcap.read()
    antal = 0
    funkar = True
    coordinates = []
    counter = 0

    _, img = vidcap.read()
    cv2.imshow('img', img)
    cv2.setMouseCallback('img', click_event, (img, coordinates))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return coordinates


if __name__ == '__main__':
    print(calCordinates('/Users/pontusjohansson/Documents/FloorballTracker/videos/personal/gear360FisheyeKarhall.mp4'))

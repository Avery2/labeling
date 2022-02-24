import time
import sys
import cv2 as cv
import csv
import pandas as pd
import os

def moveleft(n=1000):
    """Returns unicode string to move cursor left by n"""
    return u"\u001b[{}D".format(n)


def readFrame(cap, IMG_SIZE=(128, 128)):
    '''
    Reads the next frame using cap from cv2.VideoCapture
    :param cap: cv2.VideoCapture instance
    :param IMG_SIZE: size of the returned image
    :return: Returns frame and its gray analog
    '''

    ret, origFrame = cap.read()
    if not ret:
        return ret, None, None, None
    # frame = cv.resize(origFrame, IMG_SIZE)
    # gray = cv.cvtColor(origFrame, cv.COLOR_BGR2GRAY)
    # cv.imshow("origframe", origFrame)

    return ret, origFrame, origFrame, origFrame

if __name__ == '__main__':
    labels = []
    frame_i = 0
    VIDEO_PATH_DEFAULT = "videos/pushups/SideView.mp4"
    CSV_PATH_DEFAULT = "labels/SideView.csv"
    MOVEMENT_DIR_PATH_DEFAULT = "pushups_split"

    # command line parsing
    if len(sys.argv) < 5:
        print("usage: sort_frames_by_type.py video_path csv_path movement_dir_path labels")
        exit(1)

    video_path = sys.argv[1] or VIDEO_PATH_DEFAULT
    output_csv_path = sys.argv[2] or CSV_PATH_DEFAULT
    movement_dir_path = sys.argv[3] or MOVEMENT_DIR_PATH_DEFAULT
    label_characters = sys.argv[4] or "012"

    # print(f"{label_characters=}")

    up_dir_path = f"{movement_dir_path}/up/"
    down_dir_path = f"{movement_dir_path}/down/"
    unknown_dir_path = f"{movement_dir_path}/unknown/"
    filename = video_path.split(".")[-2].split("/")[-1]

    # print(f"{filename=}")

    if not os.path.exists(movement_dir_path):
        os.mkdir(movement_dir_path)

    if not os.path.exists(up_dir_path):
        os.makedirs(up_dir_path)

    if not os.path.exists(down_dir_path):
        os.makedirs(down_dir_path)

    if not os.path.exists(unknown_dir_path):
        os.makedirs(unknown_dir_path)

    movement_labels = pd.read_csv(output_csv_path)

    print(f"{movement_labels=}")

    cap = cv.VideoCapture(video_path)
    start = time.time()

    # iterate over every frame
    count = 0
    while(cap.isOpened()):
        ret, origFrame, _, _ = readFrame(cap)
        if not ret:
            print(f"{count} frames processed")
            break

        if str(movement_labels["Label"][count]) == label_characters[0]:
            cv.imwrite(f"{down_dir_path}{filename}_frame_{count}.jpg", origFrame)
            # print(f"{down_dir_path}{filename}_frame_{count}.jpg")
        elif str(movement_labels["Label"][count]) == label_characters[1]:
            cv.imwrite(f"{up_dir_path}{filename}_frame_{count}.jpg", origFrame)
            # print(f"{up_dir_path}{filename}_frame_{count}.jpg")
        elif str(movement_labels["Label"][count]) == label_characters[2]:
            cv.imwrite(f"{unknown_dir_path}{filename}_frame_{count}.jpg", origFrame)
            # print(f"{unknown_dir_path}{filename}_frame_{count}.jpg")
      
        count += 1

    end = time.time()
    print(f"\nElapsed time: {round(end - start, 5)}s {frame_i}")
    # The following frees up resources and closes all windows
    cap.release()
    cv.destroyAllWindows()

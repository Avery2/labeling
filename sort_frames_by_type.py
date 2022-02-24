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

labels = []
frame_i = 0
#FILENAME = "SideView"
#FILENAME = "FrontView"
FILENAME = "Avery-Front"
#VIDEO_PATH = f"data/{FILENAME}.mp4"

VIDEO_PATH = f"../videos/pushups/{FILENAME}.mp4"
OUTPUT_CSV_PATH = f"labels/{FILENAME}.csv"

MOVEMENT_DIR_PATH = "pushups_split"
UP_DIR_PATH = f"{MOVEMENT_DIR_PATH}/up/"
DOWN_DIR_PATH = f"{MOVEMENT_DIR_PATH}/down/"
UNKNOWN_DIR_PATH = f"{MOVEMENT_DIR_PATH}/unknown/"

if not os.path.exists(MOVEMENT_DIR_PATH):
    os.mkdir(MOVEMENT_DIR_PATH)

if not os.path.exists(UP_DIR_PATH):
    os.makedirs(UP_DIR_PATH)

if not os.path.exists(DOWN_DIR_PATH):
    os.makedirs(DOWN_DIR_PATH)

if not os.path.exists(UNKNOWN_DIR_PATH):
    os.makedirs(UNKNOWN_DIR_PATH)


movement_labels = pd.read_csv(OUTPUT_CSV_PATH)

if __name__ == '__main__':

    print(movement_labels)
    cap = cv.VideoCapture(VIDEO_PATH)
    start = time.time()


    # # iterate over every frame
    count = 0
    while(cap.isOpened()):
        ret, origFrame, _, _ = readFrame(cap)
        if not ret:
            print(f"{count} frames processed")
            break
       # cv.imshow(f"input", origFrame)
        # if set to 0 will only move forward when something is pressed
        # pressedKey = cv.waitKey(0)
        # sys.stdout.write(moveleft() + f"Pressed key {chr(pressedKey & 0xFF)} {frame_i}")
        # sys.stdout.flush()
        # if pressedKey & 0xFF == ord('q'):
        #     break

        #labels.append(chr(pressedKey & 0xFF))
       # frame_i += 1

        if str(movement_labels["Label"][count]) == "0":
          #  print("writing down")
            cv.imwrite(f"{DOWN_DIR_PATH}{FILENAME}_frame_{count}.jpg", origFrame)
        elif str(movement_labels["Label"][count]) == "1":
           # print("writing up")
            cv.imwrite(f"{UP_DIR_PATH}{FILENAME}_frame_{count}.jpg", origFrame)
        elif str(movement_labels["Label"][count]) == "2":
           # print("writing unknown")

            cv.imwrite(f"{UNKNOWN_DIR_PATH}{FILENAME}_frame_{count}.jpg", origFrame)
      
        # else:
        #     print("not writing anything")
        count += 1

    end = time.time()
    print(f"\nElapsed time: {round(end - start, 5)}s {frame_i}")
    # print(" ".join(labels))
    # The following frees up resources and closes all windows
    cap.release()
    cv.destroyAllWindows()

    # # write data
    # with open(OUTPUT_CSV_PATH, 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(("Frame", "Label"))
    #     for i, label in enumerate(labels):
    #         writer.writerow((i + 1, label))


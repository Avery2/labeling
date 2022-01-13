import sys
import cv2 as cv
import csv



def printOverwrite(s: str) -> None:
    """Prints something onn the same line, overwriting that was last written. Useful for a recurring value like a loading bar."""

    def moveleft(n=1000) -> str:
        """Returns unicode string to move cursor left by n"""
        return u"\u001b[{}D".format(n)

    sys.stdout.write(moveleft() + s)
    sys.stdout.flush()

def readFrame(cap, buff: list, redo: list):
    '''
    Reads the next frame using cap from cv2.VideoCapture
    :param cap: cv2.VideoCapture instance
    :return: Returns frame and its gray analog
    '''
    BUFF_SIZE = 50

    if (redo):
        frame = redo.pop(0)
        haveNextFrame = True
    else:
        haveNextFrame, frame = cap.read()
    if not haveNextFrame:
        return haveNextFrame, None

    if len(buff) >= BUFF_SIZE:
        buff.pop(0)
    buff.append(frame)

    return haveNextFrame, frame

if __name__ == '__main__':
    labels = []
    buff = []
    redo = []
    frame_i = 0
    FILENAME = "SideView"
    VIDEO_PATH = f"data/{FILENAME}.mp4"
    OUTPUT_CSV_PATH = f"labels/{FILENAME}.csv"
    cap = cv.VideoCapture(VIDEO_PATH)
    haveNextFrame, frame = cap.read()

    # iterate over every frame
    while(cap.isOpened()):
        if not haveNextFrame:
            break
        cv.imshow(f"input", frame)

        # if set to 0 will only move forward when something is pressed
        pressedKey = cv.waitKey(0)

        printOverwrite(f"Pressed key {chr(pressedKey & 0xFF)} {frame_i=:04} {len(labels)=:04}")

        if pressedKey & 0xFF == ord('q'):
            break
        if pressedKey & 0xFF == ord('b'):
            # TODO: implement undo
            if buff:
                lastFrame = buff.pop()
                redo.insert(0, lastFrame)
                frame = lastFrame
                haveNextFrame = True
                frame_i -= 1
                labels.pop()
        else:
            labels.append(chr(pressedKey & 0xFF))
            frame_i += 1
            haveNextFrame, frame = readFrame(cap, buff, redo)

    # The following frees up resources and closes all windows
    cap.release()
    cv.destroyAllWindows()

    # write data
    with open(OUTPUT_CSV_PATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(("Frame", "Label"))
        for i, label in enumerate(labels):
            writer.writerow((i + 1, label))


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


class LabelCreator:
    """Creates label for video."""

    def __init__(self, videoPath, buffSize=50):
        self.labels = []
        self.buffer = []
        self.redo = []
        self.frameNum = 0
        self.buffSize = buffSize
        self.cap = cv.VideoCapture(videoPath)

    def readFrame(self):
        """Reads and returns the next frame using cap from cv2.VideoCapture"""
        if (self.redo):
            frame = self.redo.pop(0)
            haveNextFrame = True
        else:
            haveNextFrame, frame = self.cap.read()
        if not haveNextFrame:
            return haveNextFrame, None
        if len(self.buffer) >= self.buffSize:
            self.buffer.pop(0)
        self.buffer.append(frame)
        return haveNextFrame, frame

    def undo(self):
        """Go backwards a frame and undo labeling"""
        if self.buffer:
            lastFrame = self.buffer.pop()
            self.redo.insert(0, lastFrame)
            self.frameNum -= 1
            self.labels.pop()
            return True, lastFrame
        return False, None

    def labelFrame(self, pressedKey):
        """Labels current frame"""
        self.labels.append(chr(pressedKey & 0xFF))
        pass

    def nextFrame(self):
        """Returns the next frame, if it exists."""
        self.frameNum += 1
        haveNextFrame, frame = self.readFrame()
        return haveNextFrame, frame

    def __del__(self):
        # The following frees up resources and closes all windows
        self.cap.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    FILENAME = "SideView"
    VIDEO_PATH = f"data/{FILENAME}.mp4"
    OUTPUT_CSV_PATH = f"labels/{FILENAME}.csv"

    lc = LabelCreator(VIDEO_PATH)
    haveNextFrame, frame = lc.cap.read()

    # iterate over every frame
    while(lc.cap.isOpened()):
        if not haveNextFrame:
            break
        cv.imshow(f"input", frame)
        pressedKey = cv.waitKey(0)  # if set to 0 will only move forward when something is pressed
        printOverwrite(f"Pressed key {chr(pressedKey & 0xFF)} {lc.frameNum=:04} {len(lc.labels)=:04}")

        if pressedKey & 0xFF == ord('q'):
            break
        elif pressedKey & 0xFF == ord('b'):
            haveNextFrame, frame = lc.undo()
        else:
            lc.labelFrame(pressedKey)
            haveNextFrame, frame = lc.nextFrame()

    # write data
    with open(OUTPUT_CSV_PATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(("Frame", "Label"))
        for i, label in enumerate(lc.labels):
            writer.writerow((i + 1, label))

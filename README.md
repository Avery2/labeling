# Labeling

## Label Instructions

The label creator will take in a video and help to label each frame. It will pause the video, and only continue to the next frame once you press a key which will be the label for that frame. You can hold a key down to label many frames in sequence. The resulting labeled frames will be exported as a CSV file. 

- To run: `python label_creator.py`
- To change file change value of `VIDEO_PATH` in `label_creator.py`
- Press any character to apply label to current frame (hold key to label multiple)
- To change output CSV path change `OUTPUT_CSV_PATH` in `label_creator.py`
- Press `b` to go backwards a few frames and undo labels you did. The buffer is 100 frames but you can change this.

### Sorting frames into folders of images

- Change filename in `sort_frames_by_type.py`
- Run `python3 sort_frames_by_type.py`

# Labeling

## Label Instructions

The label creator will take in a video and help to label each frame. It will pause the video, and only continue to the next frame once you press a key which will be the label for that frame. You can hold a key down to label many frames in sequence. The resulting labeled frames will be exported as a CSV file. 

Usage: `python label_creator.py video_path output_csv_path`

- Press any character to apply label to current frame (hold key to label multiple)
- Press `b` to go backwards a few frames and undo labels you did. The buffer is 100 frames but you can change this.

### Sorting frames into folders of images

Usage: `sort_frames_by_type.py video_path csv_path movement_dir_path labels`

- `labels` shouold be a length 3 string are by default `012`
- Run `python3 sort_frames_by_type.py`

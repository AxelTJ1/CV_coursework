import cv2
import numpy as np

# function used to extract frames from a video
# skipFrames: number of frames to skip between each frame that is taken
# maxFrames: total number of frames to extract
# resizeWidth: width to resize each frame to (maintains aspect ratio)
def extractFrames(videoPath, skipFrames=30, maxFrames=5, resizeWidth=640):
    video = cv2.VideoCapture(videoPath)
    frames = []
    frame_idx = 0

    while video.isOpened():
        ret, frame = video.read()
        if not ret or len(frames) >= maxFrames:
            break

        
        if frame_idx % skipFrames == 0:
            # rotate frames 90 degrees because test videos recorded in portrait, if video is recorded in landscape then comment this out
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            h, w = frame.shape[:2]
            new_h = int(h * (resizeWidth / w))
            frame = cv2.resize(frame, (resizeWidth, new_h))

            frames.append(frame)

        frame_idx += 1

    video.release()
    return frames

# function used to stitch the frames
def stitch(frames):
    if len(frames) < 2:
        print("Unable to stitch less than 2 frames.")
        return None

    # create stitcher object and stitch the frames
    stitcher = cv2.Stitcher_create()
    status, panorama = stitcher.stitch(frames)

    if status != cv2.Stitcher_OK:
        print(f"Failed to stitch.")
        return None

    return panorama

# main function
# prompts the user to enter the name of the video
fileName = input("Enter the video file name (without extension): ")
if not fileName.lower().endswith(('.mp4', '.avi', '.mov')):
    fileName += ".mp4"
videoFile = fileName

# extract the frames to be used for panorama generation
frames = extractFrames(videoFile, skipFrames=10, maxFrames=15)

result = stitch(frames)

if result is not None:
    cv2.imwrite('panorama.jpg', result)
    print("Panorama has been generated, saved as panorama.jpg")
else:
    print("Panorama generation failed.")

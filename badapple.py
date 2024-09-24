# get pixels from image

from PIL import Image
import numpy as np
import cv2
import time
import os
from os.path import exists

def get_pixels(image_path):
    im = Image.open(image_path)
    im = im.convert('L') # convert to grayscale
    im = im.resize((80, 45)) # resize to 80x45
    pixels = np.array(im) # convert to numpy array
    return pixels

def get_ascii(pixels):
    ascii_chars = " .,:;irsXA253hMHGS#9B&@" # 0-255
    ascii_pixels = [] 
    for row in pixels:
        ascii_row = []
        for pixel in row:
            ascii_row.append(ascii_chars[pixel // 25]) # 25 = 256 / 10
        ascii_pixels.append(ascii_row)
    return ascii_pixels

def print_ascii(ascii_pixels):
    for row in ascii_pixels:
        print(''.join(row))

# get frame from video
def getFrames(path):
    cap = cv2.VideoCapture(path) # open video
    current_frame = 0
    while cap.isOpened():
        ret, frame = cap.read() # read frame
        if ret: # if frame is read correctly
            if(not exists(f"badappleFrame/frame{current_frame}.jpg")): 
                cv2.imwrite(f"badappleFrame/frame{current_frame}.jpg", frame) # save frame
            current_frame += 1
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

# Main
if not os.path.exists("badappleFrame"):
   os.mkdir("badappleFrame")
getFrames("badapple.mp4")

for i in range(len(os.listdir('badappleFrame/'))):
    print_ascii(get_ascii(get_pixels(f"badappleFrame/frame{i}.jpg")))
    # 24 fps
    time.sleep(1/24)
    #clear screen
    #os.system("cls")
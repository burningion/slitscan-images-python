import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="filename to generate slit scan image from")
args = parser.parse_args()

from moviepy.editor import VideoFileClip, VideoClip
from PIL import Image

import numpy as np

clip = VideoFileClip(args.filename).resize(0.2)

print('%s is %i fps, for % seconds at %s' % (args.filename, clip.fps, clip.duration, clip.size))

img = np.zeros((clip.size[1], clip.size[0], 3), dtype='uint8')

currentX = 0
slitwidth = 1

slitpoint = clip.size[1] // 2

frame_generator = clip.iter_frames(fps=clip.fps, dtype='uint8')

def make_frame(t):
    global img, currentX
    next_frame = next(frame_generator)
    img = np.roll(img, -1, axis=0)
    img[slitpoint,:,:] = next_frame[slitpoint,:,:]
    next_frame[max(slitpoint - currentX, 0):slitpoint,:,:] = img[max(0, slitpoint - currentX):slitpoint,:,:]

    currentX += 1
    return next_frame

output = VideoClip(make_frame=make_frame, duration=10.5)
output.write_gif('output1.gif', fps=12)

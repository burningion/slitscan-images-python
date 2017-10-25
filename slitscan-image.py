import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="filename to generate slit scan from")
args = parser.parse_args()

print('opening file %s for slit scanning' % args.filename)

from moviepy.editor import VideoFileClip
import numpy as np

from PIL import Image

clip = VideoFileClip(args.filename)

print('%s is %i fps, for %i seconds at %s' % (args.filename, clip.fps, clip.duration, clip.size))

# np.zeros is how we generate an empty ndarray
img = np.zeros((clip.size[1], clip.size[0], 3), dtype='uint8')

currentX = 0
slitwidth = 1

slitpoint = clip.size[0] // 2

# generate our target fps with width / duration
target_fps = clip.size[0] / clip.duration

for i in clip.iter_frames(fps=target_fps, dtype='uint8'):
    if currentX < (clip.size[0] - slitwidth):
        img[:,currentX:currentX + slitwidth,:] = i[:,slitpoint:slitpoint+slitwidth,:]
    currentX += slitwidth

output = Image.fromarray(img)
output.save('output_post.jpg')

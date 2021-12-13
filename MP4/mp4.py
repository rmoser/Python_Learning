import ffmpy
import os

inp = {r"D:\Temp\YMNB-lesson08-20170519-final.mp4": None}
outp = {r"D:\Temp\YMNB-lesson08-20170519-small.mp4": '-vcodec libx265 -crf 24'}
ff = ffmpy.FFmpeg(inputs=inp, outputs=outp)
print(ff.cmd)

ff.run()


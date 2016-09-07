import numpy as np
import h5py
import scisoftpy as dnp
from time import sleep
from math import cos, sin

print("Starting")

data = h5py.File('/dls/tmp/ssg37927/31_processed_160905_141219.nxs','r')['entry/result/data']
angles = h5py.File('/dls/tmp/ssg37927/31_processed_160905_141219.nxs','r')['entry/result/Angle']

frame = 300
dnp.plot.image(data[:,frame,:])

cor = 140
pad = 50
xs, ys = np.meshgrid(np.arange(data.shape[0]+(2*pad))-(cor+pad), np.arange(data.shape[0]+(2*pad))-(cor+pad))

dnp.plot.image(xs, name='xs')
dnp.plot.image(ys, name='ys')


result = np.zeros([data.shape[1]]+list(xs.shape))

#dnp.plot.image(result, name='result')

angles = np.deg2rad(angles)



for f in range(100,data.shape[1]):
    print("F is ", f)

    dnp.plot.image(data[:,f,:])

    for i in range(angles.shape[0]):
        angle = angles[i]
        #print("Angle : ", angle)
        xx = xs*cos(angle) - ys*sin(angle)
        xx = xx.astype(np.int16) + (cor+pad)
        xx[xx>data.shape[0]-1] = data.shape[0]-1
        #yy = ys*cos(angle) + xs*sin(angle)

        #dnp.plot.image(xx, name='xx')
        #dnp.plot.image(yy, name='yy')

        stripe = data[i,f,:][xx]

        #dnp.plot.image(stripe, name='stripe')

        result[f,:,:] = result[f,:,:] + stripe

    dnp.plot.image(result[f,:,:], name='result')

print("Opening file")

output = h5py.File('/dls/tmp/ssg37927/mb1.h5','w')
output.create_dataset("data", data=result)
output.close()

print("Done")

import numpy as np
import os.path
from image_op import readimage_batch
from scipy.misc import imsave 
from background_del import background_del

indir = "D:/CsTech/CV/image/portrait"
outdir = "D:/CsTech/CV/image/bgdel"
x, name = readimage_batch(indir)

if not os.path.exists(outdir):
    os.mkdir(outdir) 

N = len(x)
for i in xrange(N):
    x_bgdel = background_del(x[i])
    print '%s is done' %name[i]
    imsave(outdir +'/'+ name[i], x_bgdel)
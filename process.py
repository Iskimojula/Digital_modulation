import numpy
import maskproc
import psfproc
import pylab
from datetime import datetime
import cv2
import os

show = True

#mask para.
convsize = 21
step_in_deg = 36
step_in_radial = 16
radius0 = 128
mask_type = 'IMPORT'

timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

source_img,output_img,pupil_radius,Me = psfproc.psfprocess()
imgshape = output_img.shape[0]

mask  = maskproc.make_mask(imgshape,step_in_deg,step_in_radial,radius0,convsize,mask_type)

modulate_img = numpy.zeros_like(output_img,dtype = numpy.uint8)

for i in range(modulate_img.shape[2]):
    modulate_img[:,:,i] = output_img[:,:,i] * (mask/255) + source_img[:,:,i] * (1-mask/255)

figurename = "pupil_radius_" + str(pupil_radius*1000) + " Me_" + str(Me) + " GaussianSize_" + str(convsize)

if show :
    pylab.figure(num=figurename,figsize=(12,10))
    pylab.subplot(2,2,1)
    pylab.title("original image")
    pylab.imshow(source_img,interpolation='nearest')

    pylab.subplot(2,2,2)
    pylab.title("mask")
    pylab.imshow(mask,cmap='gray',interpolation='nearest')

    pylab.subplot(2,2,3)
    pylab.title("psf conv. image")
    pylab.imshow(output_img,interpolation='nearest')

    pylab.subplot(2,2,4)
    pylab.title("modulation image")
    pylab.imshow(modulate_img,interpolation='nearest')
    
    
    savefigurename = figurename + "_ts_" + timestamp + ".jpg"

    savefigurepath = os.path.join('output_modulation',savefigurename)
    pylab.savefig(savefigurepath)

    writeresname = "res_" + savefigurename
    writerespath = os.path.join('output_modulation',writeresname)
    cv2.imwrite(writerespath,modulate_img)

    pylab.show()
 

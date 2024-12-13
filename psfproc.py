import aberrationRendering
import imageproc
from aberrationRendering import Zernike
import numpy
import pylab
import cv2
import math
import os
def psfprocess():
    debug = 0

    layerindex = ["blue" , "green" ,"red"]

    # Wavefront representation
    array_size = 512
    n_radial_orders = 5
    pupil_radius = 1.5e-3

    z = Zernike(print_indices = True)

    r = z.r
    theta = z.theta
    indices = z.index_mapping
    zernike_matrix = z.zernike_matrix


    Me = 1
    RMS = Me * pow(pupil_radius,2)/(4*math.sqrt(3))
    '''
    We can represent any wavefront error by computing the matrix multiplication of the Zernike matrix with the Zernike
    coefficient vector.
    '''
    zernike_coefficients = numpy.zeros(zernike_matrix.shape[0])
    zernike_coefficients[4] = RMS
    #zernike_coefficients[12] = 0.3e-6
    wavefront_error = aberrationRendering.wavefront(zernike_coefficients,zernike_matrix)


    #pylab.figure(1)
    #pylab.imshow(wavefront_error, interpolation='nearest', cmap='gray')

    '''
    we specify the pupil amplitude function
    '''
    amplitude_function = aberrationRendering.amplitudeFunctionCircle(array_size)

    #pylab.figure(2)
    #pylab.imshow(amplitude_function, interpolation='nearest', cmap='gray')


    '''
    check that there are a sufficient number of pixels across the wavefront
    '''
    oversampling = 2
    wavefront_gradient_check,psf_fov_check = \
    aberrationRendering.checkSampling(wavefront_error,amplitude_function,array_size,oversampling)
    print("wavefront_gradient_check : ",wavefront_gradient_check)
    print("psf_fov_check : ", psf_fov_check)


    #PSF generation
    '''
    The PSF is the Fourier transform of the complex pupil function
    '''
    wavelength = 550e-9

    psf = aberrationRendering.PSF(wavefront_error, amplitude_function, wavelength=wavelength, oversampling= oversampling)
    print("psf_size : ", psf.shape)
    #pylab.figure(3)
    #pylab.imshow(psf, interpolation='nearest', cmap='gray')

    psf_diffraction_limited = aberrationRendering.PSF(zernike_matrix[0]*0.0, amplitude_function, wavelength=wavelength, oversampling= oversampling)

    #Convolution of the PSF with an input intensity pattern
    pixel_scale = aberrationRendering.psfPixelScale(wavelength=wavelength,oversampling=oversampling,pupil_radius=pupil_radius)
    pixel_scale_arcminutes = pixel_scale * 180 * 60/ numpy.pi

    print("pixel_scale : ",pixel_scale)
    print("pixel_scale_arcminutes : ", pixel_scale_arcminutes)

    field_of_view_arcminutes = 7.56*60
    n_pixels = aberrationRendering.numberPixels(field_of_view_arcminutes,
    wavelength=wavelength,oversampling = oversampling,pupil_radius=pupil_radius)

    layer=0 
    n_pixels = 1024
    square = numpy.zeros((n_pixels,n_pixels,3),numpy.uint8)
    if 0 :
        output_cropped = numpy.zeros_like(square)
        for layer in range(3):
            
            square[:,:,layer] = numpy.ones((n_pixels,n_pixels),numpy.uint8) * 255
            square[int(n_pixels/4):int(n_pixels*3/4),int(n_pixels/4):int(n_pixels*3/4),layer] = 0

            square_full = numpy.ones((psf.shape),numpy.uint8)*255
            square_full[:square.shape[0],:square.shape[1]] = square[:,:,layer]
            output_intensity_pattern = aberrationRendering.convolveImage(square_full,psf)
            output_cropped[:,:,layer]= output_intensity_pattern[:square.shape[0],:square.shape[1]]


        cv2.imwrite('original_image.jpg',square)
        cv2.imwrite('psf_image.jpg',output_cropped)

        show_original_image = pylab.imread('original_image.jpg')
        show_psf_image = pylab.imread('psf_image.jpg')

        pylab.figure(1)
        pylab.subplot(1,2,1)
        pylab.title("original image")
        pylab.imshow(show_original_image)

        pylab.subplot(1,2,2)
        pylab.title("psf image")
        pylab.imshow(show_psf_image)
        pylab.show()


    if 1:
        '''
        image process
        '''
        imageprocess = imageproc.ImgProc("sample.jpg",n_pixels,n_pixels)

        output_cropped = numpy.zeros_like(imageprocess.image)

        for i in range(imageprocess.image.shape[2]):
            
            square_full = numpy.ones((psf.shape),numpy.uint8)*255
            square_full[:square.shape[0],:square.shape[1]] = imageprocess.image[:,:,i]
            output_intensity_pattern = aberrationRendering.convolveImage(square_full,psf)
            output_cropped[:,:,i] = output_intensity_pattern[:imageprocess.image.shape[0],:imageprocess.image.shape[1]]

        
        if debug :
            cv2.imwrite('original_image.jpg',imageprocess.image)
            if Me:
                psf_image_name = "oversampleing_" + str(oversampling) + " pupil_radius_" + str(pupil_radius * 1000) + " Me_" + str(Me) + " RMS_" + f"{RMS* 1e6:.3f}" + ".jpg"
            else:
                psf_image_name = "oversampleing_" + str(oversampling) + " pupil_radius_" + str(pupil_radius * 1000) + ".jpg"
                

            psf_image_path = os.path.join("output" , psf_image_name)
            cv2.imwrite(psf_image_path,output_cropped)
            cv2.imwrite('psf_image.jpg',output_cropped)
            show_original_image = pylab.imread('original_image.jpg')
            show_psf_image = pylab.imread('psf_image.jpg')

            figurename = "oversampleing_" + str(oversampling) + " pupil_radius_" + str(pupil_radius * 1000)
            pylab.figure(num=figurename)
            pylab.subplot(2,4,1)
            pylab.title("original image")
            pylab.imshow(show_original_image)

            pylab.subplot(2,4,2)
            pylab.title("original image blue")
            pylab.imshow(show_original_image[:,:,0],cmap='gray')
            pylab.subplot(2,4,3)
            pylab.title("original image green")
            pylab.imshow(show_original_image[:,:,1],cmap='gray')
            pylab.subplot(2,4,4)
            pylab.title("original image red")
            pylab.imshow(show_original_image[:,:,2],cmap='gray')

            pylab.subplot(2,4,5)
            pylab.title("psf image")
            pylab.imshow(show_psf_image)


            pylab.subplot(2,4,6)
            pylab.title("psf image blue")
            pylab.imshow(show_psf_image[:,:,0],cmap='gray')
            pylab.subplot(2,4,7)
            pylab.title("psf image green")
            pylab.imshow(show_psf_image[:,:,1],cmap='gray')
            pylab.subplot(2,4,8)
            pylab.title("psf image red")
            pylab.imshow(show_psf_image[:,:,2],cmap='gray')

            pylab.show()

    return imageprocess.image,output_cropped,pupil_radius,Me
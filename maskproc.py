import cv2
import numpy as np
import math

def Polar2Cart(polar_radius, polar_deg):
    x = round(polar_radius * math.cos(math.radians(polar_deg)))
    y = round(polar_radius * math.sin(math.radians(polar_deg)))
    return x , y   

def make_mask(size,step_in_deg,step_in_radial,radius0,convsize = 7,mask_type = 'DSDO'):
    mask_size = size #1024
    mask = np.zeros((mask_size,mask_size),dtype = np.uint8)

    step_in_deg = step_in_deg #32
    step_in_radial = step_in_radial #8

    center_coordinates0 = (int(mask_size/2),int(mask_size/2))
    radius0 = radius0 #128
    color = 255
    thickness = -1
    #cv2.circle(mask,center_coordinates0,radius0,color,thickness)
    defocuscluster_num =  step_in_deg
    defocuscluster_Deg =  360/defocuscluster_num

    if mask_type == 'DSDO' :
        defocuslens_radius0 = int(radius0 * math.tan(math.radians(defocuscluster_Deg/2)))
        print("defocuslens_radius :" , defocuslens_radius0)

        for i in range(defocuscluster_num):
            for j in range(step_in_radial):
                Polar_radius = math.sqrt(pow(defocuslens_radius0,2) + pow(radius0,2)) + j*defocuslens_radius0*2
                
                Polar_Deg = i*defocuscluster_Deg
                relative_x , relative_y = Polar2Cart(Polar_radius,Polar_Deg)
                image_x = center_coordinates0[0] + relative_x
                image_y = center_coordinates0[0] - relative_y
                cv2.circle(mask,(image_x,image_y),defocuslens_radius0,color,thickness)

        mask = cv2.GaussianBlur(mask,(convsize,convsize),0)
        return mask
    elif mask_type == 'IMPORT':
        threshold_value = 128
        mask = cv2.imread('mask.jpg',cv2.IMREAD_GRAYSCALE)
        _, binary_image = cv2.threshold(mask, threshold_value, 255, cv2.THRESH_BINARY)
        mask = binary_image
        mask = cv2.GaussianBlur(mask,(convsize,convsize),0)
        return mask
            
        
'''
if __name__ == "__main__":
    mask = make_mask(1024,18,8,128,9,'IMPORT')    
    cv2.imshow('Image Window',mask)
    cv2.waitKey(0)
    cv2.destoryAllWindows()
'''
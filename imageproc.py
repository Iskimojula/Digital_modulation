import cv2

class ImgProc:
    def __init__(self,image_path,image_width,image_height,label = 'rgb'):
        self.sample_path = image_path
        self.image_width  = image_width
        self.image_height = image_height
        self.label = label
        self.__CropSample()

    def __CropSample(self):
        sample_img = cv2.imread(self.sample_path)
        height,width,_ = sample_img.shape

        if height < self.image_height or width < self.image_width:
            print(" Sampe size error !!!")
            print("n_pixel: ", self.image_width, self.image_height)
            exit() 

        '''
        center_x,center_y = width//2, height//2

        x1 = center_x - self.image_width // 2
        y1 = center_y - self.image_height // 2
        x2 = center_x + self.image_width // 2
        y2 = center_y + self.image_height // 2
        '''

        self.image = sample_img[0:self.image_height,0:self.image_width]
        
        print("n_pixel_size, height: ", self.image_height ,  "width: ", self.image_width)
        print("image size: ", self.image.shape[:2])

        #cv2.imshow('resize image',self.image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
            
def checkimage(image):
    for layer in range(image.shape[2]-1):
        pass



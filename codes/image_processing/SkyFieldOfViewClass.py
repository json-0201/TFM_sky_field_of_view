import numpy as np, cv2, os
from region_growth_method import *


def load_images(folder: str) -> list:
    """load images from a directory"""

    images = []

    for file in range(len(os.listdir(folder))):
        image = os.listdir(folder)[file]
        images.append(image)

    return images


class SkyFieldView:
    '''include all methods for SFV calculation'''


    def __init__(self, file: str):
        '''Initialize, load an image'''

        self.image = cv2.imread(file, cv2.IMREAD_COLOR)
        self.name = file


    def rescale_image(self, percent: int = 15) -> cv2.Mat:
        '''rescale image to input percent'''

        width = int(self.image.shape[0] * percent / 100)
        height = int(self.image.shape[1] * percent / 100)
        dim = (width, height)

        rescaled_image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)
        # self.show_image(rescaled_image, self.name)

        return rescaled_image
    

    def mask_circle(self, image: cv2.Mat) -> cv2.Mat:
        '''create circular mask to apply on image'''

        X, Y, _ = image.shape
        radius = int((image.shape[0]/2) + 10)
        center = (int(X/2), int(Y/2))
        rect = np.zeros((X, Y), dtype = np.uint8)

        circle_gray = cv2.circle(rect, center, radius, (255, 255, 255), thickness = -1)
        circle_bgr = self.gray2bgr(circle_gray)
        # self.show_image(circle_bgr, self.name)

        return circle_bgr


    def mask_sky_bgr(self, image: cv2.Mat) -> cv2.Mat:
        """create a sky filter using inRange()"""

        b = cv2.inRange(image[:,:,0], 85, 255)
        g = cv2.inRange(image[:,:,1], 0, 65)
        r = cv2.inRange(image[:,:,2], 0, 65)

        no_sky1 = cv2.bitwise_or(g, r)
        no_sky2 = cv2.bitwise_not(b)
        no_sky = cv2.bitwise_or(no_sky1, no_sky2)
        sky = cv2.bitwise_not(no_sky)
        sky = self.gray2bgr(sky)
        
        sky[np.all(sky == (255, 255, 255), axis = -1)] = (255, 0, 255)
        
        # self.show_image(sky, self.name)

        return sky


    def mask_sky_rgm(self, image: cv2.Mat) -> cv2.Mat:
        """region growth method sky filter"""

        sky_mask_gray = self.bgr2gray(image)
        
        seeds = [Point(328,328),Point(328,348),Point(328,368),\
        Point(348,328),Point(348,348),Point(348, 368),\
        Point(368,328),Point(368,348),Point(368,328)]

        sky_mask_gray = regionGrow(sky_mask_gray, seeds, 5)
        sky_mask_rgm = self.convert_image(sky_mask_gray, 0, 255, np.uint8)
        sky_mask_rgm = self.gray2bgr(sky_mask_rgm)
        sky_mask_rgm[np.all(sky_mask_rgm == (255, 255 ,255), axis = -1)] = (255, 0, 255)

        return sky_mask_rgm
        

    def sky_ratio(self, sky: cv2.Mat, circle: cv2.Mat) -> int:
        """calculate SFV(%) of input image"""
        
        img_sky = self.bgr2gray(sky)
        img_circle = self.bgr2gray(circle)

        sky_area = cv2.countNonZero(img_sky)
        circle_area = cv2.countNonZero(img_circle)

        sfv = int(sky_area / circle_area * 100)
        print("sfv:", str(sfv) + "%")
        
        return sfv


    @staticmethod
    def save_images(image: cv2.Mat, name: str, folder: str):
        """save images to a directory"""

        cv2.imwrite(os.path.join(folder, f"{name}"), image)


    @staticmethod # when self is not needed
    def show_image(image, name):
        cv2.imshow(f'{name}', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    
    @staticmethod
    def gray2bgr(image):
        '''convert grayscale format image to bgr'''

        image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        return image_bgr
    

    @staticmethod
    def bgr2gray(image):
        '''convert bgr format image to grayscale'''

        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        return image_gray

    
    @staticmethod
    def apply_mask(image, mask):
        '''operate bitwise_and() function on two input images'''

        masked_image = cv2.bitwise_and(image, mask)
        
        return masked_image

    
    @staticmethod
    def convert_image(image, target_type_min, target_type_max, target_type):
        '''convert image with input target parameters'''
            
        imin = image.min()
        imax = image.max()

        a = (target_type_max - target_type_min) / (imax - imin)
        b = target_type_max - a * imax
        new_image = (a * image + b).astype(target_type)
        
        return new_image
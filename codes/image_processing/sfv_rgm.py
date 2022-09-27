import pandas as pd, os
from SkyFieldOfViewClass import SkyFieldView, load_images
from constants import *

# load images from image directory
images = load_images(IMAGE_PATH)

# load csv to record sfv
df = pd.read_csv("parking_lat_long_alt.csv", index_col="parking_undistorted-[i].jpg")

# loop thorugh each image
for file in images:
    
    os.chdir(IMAGE_PATH)

    image = SkyFieldView(file)
    rescaled_image = image.rescale_image()
    circle_mask = image.mask_circle(rescaled_image)
    masked_image = image.apply_mask(rescaled_image, circle_mask)
    sky_mask = image.mask_sky_rgm(masked_image)
    image.save_images(sky_mask, file, FILTER_PATH_RGM)
    sky_image = image.apply_mask(masked_image, sky_mask)
    image.save_images(sky_image, file, FILTERED_PATH_RGM)
    sfv = image.sky_ratio(sky_image, circle_mask)
    df.loc[file, "SFV(%)"] = sfv

df.to_csv(RESULT_PATH + "\sfv_rgm.csv")
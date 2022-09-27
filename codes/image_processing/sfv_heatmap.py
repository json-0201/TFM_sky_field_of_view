# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 15:21:28 2022

@author: Jimmy Son
"""

import numpy as np, pandas as pd, cv2, matplotlib.pyplot as plt
from scipy.interpolate import griddata
import seaborn as sb; sb.set_theme()


# load csv
PATH = r'C:\Users\Jimmy Son\Desktop\PROGRAM\CS\Python\projects\TFM\scipy'
df = pd.read_csv(PATH + '\parking_pixel_coordinates.csv', index_col = 'parking_undistorted-[i].jpg',)


# create nd-array of zeros with google map parking lot capture resolution
parking_all = np.zeros(shape=(885, 690))


parking_row = []
parking_col = []
parking_sfv = []

for ind in df.index:
    parking_row.append(df['pixel_row'][ind])
    parking_col.append(df['pixel_col'][ind])
    parking_sfv.append(df['SFV(%)'][ind])


# add SFV to empty arrays
pixel_parking = zip(parking_row, parking_col)

ind = 0
for r, c in pixel_parking:
    parking_all[r][c] = parking_sfv[ind]
    ind += 1

 
# interpolate using scipy - parking_front
parking_width = np.linspace(0, 690, 891)
parking_height = np.linspace(0, 885, 1086)

pixel_row = np.array(parking_row)
pixel_col = np.array(parking_col)
parking_sfv_array = np.array(parking_sfv)

x_grid, y_grid = np.meshgrid(parking_width, parking_height)
z_grid = griddata((pixel_col, pixel_row), parking_sfv_array, (x_grid, y_grid), method = 'linear')

fig, ax = plt.subplots(figsize=(15, 20))
sb.heatmap(z_grid, xticklabels=False, yticklabels=False, cbar_kws={'label': 'SFV(%)'})
plt.show()

# cv2.imshow('parking',z_grid)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# repeat interpolate
parking_width = np.linspace(0, 690, 691)
parking_height = np.linspace(0, 885, 886)

parking_row_2 = []
parking_col_2 = []
parking_sfv_2 = []

for i in range(len(z_grid)):
    for j in range(len(z_grid[0])):
        if np.isnan(z_grid[i][j]) != True:
            parking_col_2.append(j)
            parking_row_2.append(i)
            parking_sfv_2.append(z_grid[i][j])

pixel_row_2 = np.array(parking_row_2)
pixel_col_2 = np.array(parking_col_2)
parking_sfv_array_2 = np.array(parking_sfv_2)
        
x_grid, y_grid = np.meshgrid(parking_width, parking_height)
z_grid_2 = griddata((pixel_col_2, pixel_row_2), parking_sfv_array_2, (x_grid, y_grid), method = 'nearest')

# hide building pixels
for i in range(250, 405):
    for j in range(40, 690):
        z_grid_2[i][j] = 0
        
for i in range(405, 550):
    for j in range(40, 255):
        z_grid_2[i][j] = 0

for i in range(680, 730):
    for j in range(250, 560):
        z_grid_2[i][j] = 0

for i in range(730, 860):
    for j in range(250, 325):
        z_grid_2[i][j] = 0        

for i in range(730, 885):
    for j in range(325, 690):
        z_grid_2[i][j] = 0   


fig, ax = plt.subplots(figsize=(15, 20))
sb.heatmap(z_grid_2, cmap = 'coolwarm', xticklabels=False, yticklabels=False, cbar_kws={'label': 'SFV(%)'})
ax.figure.axes[-1].yaxis.label.set_size(40)
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=40)
plt.show()

# cv2.imshow('parking_2',z_grid_2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
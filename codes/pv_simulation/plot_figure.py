# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 18:32:06 2022

@author: Jimmy Son
"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from constants import *

df = pd.read_csv(RESULT_PATH + '\parking_undistorted-78_iso_sfv.csv', index_col = 'utc_time', )
inc_june_15 = pd.read_csv(RESULT_PATH + '\SFV_increment_june_15.csv', index_col = 'SFV(%)', )
inc_all_year = pd.read_csv(RESULT_PATH + '\SFV_increment_all_year.csv', index_col = 'SFV(%)', )
plt.style.use('classic')


# POA Irradiance plot
plt.figure(figsize=(15,7.5))
plt.scatter(df.index, df['poa_global_sfv'], color = 'red')
plt.plot(df.index, df['poa_global_sfv'], color = 'red',  label = 'poa_global')
plt.scatter(df.index, df['poa_direct_sfv'], color = 'blue')
plt.plot(df.index, df['poa_direct_sfv'], color = 'blue', label = 'poa_direct')
plt.scatter(df.index, df['poa_diffuse_sfv'], color = 'orange')
plt.plot(df.index, df['poa_diffuse_sfv'], color = 'orange', label = 'poa_diffuse')
plt.legend(loc = 'upper left')
plt.xlabel('time')
plt.ylabel('irradiance (W/m2)')
plt.grid()
plt.show()


# TMY plot
plt.figure(figsize=(15,7.5))
plt.scatter(df.index, df['ghi'], color = 'purple')
plt.plot(df.index, df['ghi'], color = 'purple', label = 'GHI')
plt.scatter(df.index, df['dni'], color = 'brown')
plt.plot(df.index, df['dni'], color = 'brown', label = 'DNI')
plt.scatter(df.index, df['dhi'], color = 'green')
plt.plot(df.index, df['dhi'], color = 'green', label = 'DHI')
plt.legend(loc = 'upper left')
plt.xlabel('time')
plt.ylabel('irradiance (W/m2)')
plt.grid()
plt.show()


# Energy plot
w = 0.4
x = ["04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", 
     "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
prod = [-0.075, -0.075, 27.39879675, 68.4486292, 108.0146105, 140.0398553, 164.2117587, 
        178.6006627, 181.9896952, 181.4664259, 166.7513583, 147.6677145, 118.2841408, 81.07533704, 40.00013711, 5.311539989, -0.075]
prod_sfv = [-0.075, -0.075, 17.85138388, 55.00432909, 92.17338116, 123.5360481, 
            148.4261101, 164.0646862, 166.8628995, 170.2342546, 152.7337084, 134.2699309, 104.4334429, 68.03025455, 30.09585272, 1.983896443, -0.075 ]

bar1 = np.arange(len(x))
bar2 = [i+w for i in bar1]

plt.figure(figsize=(20,10))
plt.bar(bar1, prod, w, label = 'production_isotropic', color = 'red')
plt.bar(bar2, prod_sfv, w, label = 'production_sfv', color = 'orange')
plt.xlim([2,4])
plt.xlabel("time")
plt.ylabel("energy (Wh)")
plt.xticks(bar1+w/2, x)
plt.legend()
plt.grid()
plt.show()


# POA diffuse plot for both models
plt.figure(figsize=(15,7.5))
plt.scatter(df.index, df['poa_diffuse_sfv'], color = 'orange')
plt.plot(df.index, df['poa_diffuse_sfv'], color = 'orange',  label = 'poa_diffuse_sfv')
plt.scatter(df.index, df['poa_diffuse'], color = 'red')
plt.plot(df.index, df['poa_diffuse'], color = 'red', label = 'poa_diffuse_isotropic')
plt.legend(loc = 'upper left')
plt.xlabel('time')
plt.ylabel('irradiance (W/m2)')
plt.grid()
plt.show()


# PV production vs Incrementing SFV - June 15th
plt.figure(figsize=(15,7.5))
plt.scatter(inc_all_year.index, inc_all_year['%change'], color = 'orange')
plt.plot(inc_all_year.index, inc_all_year['%change'], color = 'orange',  label = 'all year')
plt.scatter(inc_june_15.index, inc_june_15['%change'], color = 'red')
plt.plot(inc_june_15.index, inc_june_15['%change'], color = 'red', label = 'june 15th')
plt.legend(loc = 'upper left')
plt.xlabel('SFV(%)')
plt.ylabel('% reduction in PV production')
plt.grid()
plt.show()
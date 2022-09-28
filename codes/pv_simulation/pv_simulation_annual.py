# -*- coding: utf-8 -*-
"""
general solar performance calculator

Created on Fri Jun  3 02:12:22 2022
@author: Jimmy Son
"""

import pvlib, pandas as pd, matplotlib.pyplot as plt
from constants import *


df = pd.read_csv(CSV_PATH + '\parking_pixel_coordinates.csv', index_col = 'parking_undistorted-[i].jpg', )


# latitude, longitude, name, altitude, timezone
altitude = ALTITUDE
timezone = TIMEZONE


# append all coordinates from csv
coordinates = []
for (idx, row) in df.iterrows():
    latitude = row.loc['latitude']
    longitude = row.loc['longitude']
    name = idx
    coordinate = (latitude, longitude, name, altitude, timezone)
    coordinates.append(coordinate)


# append all SFV values from csv
SFV = []
for ind in range(df.shape[0]):
    sky_field_of_view = int(df['SFV(%)'][ind])
    SFV.append(sky_field_of_view)


# get the module and inverter specifications from SAM
sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
sapm_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')

module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
inverter = sapm_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']

temperature_model_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']


'''
In this example we will be using PVGIS, one of the data sources available,
to retrieve a Typical Meteorological Year (TMY) which includes irradiation, temperature and wind speed
'''


# tmys collect data for one year
tmys = []
for location in coordinates:
    latitude, longitude, name, altitude, timezone = location
    weather = pvlib.iotools.get_pvgis_tmy(latitude, longitude,
                                          map_variables=True)[0]
    weather.index.name = "utc_time"
    tmys.append(weather)


# apply SFV for each coordinate
for ind in range(len(tmys)):
    tmys[ind]['dhi'] = tmys[ind]['dhi'] * SFV[ind] / 100



system = {'module': module, 'inverter': inverter,
          'surface_azimuth': 0}
energies = {}


for location, weather in zip(coordinates, tmys):
    latitude, longitude, name, altitude, timezone = location
    system['surface_tilt'] = 0
    solpos = pvlib.solarposition.get_solarposition(
        time=weather.index,
        latitude=latitude,
        longitude=longitude,
        altitude=altitude,
        temperature=weather["temp_air"],
        pressure=pvlib.atmosphere.alt2pres(altitude),
    )
    dni_extra = pvlib.irradiance.get_extra_radiation(weather.index)
    airmass = pvlib.atmosphere.get_relative_airmass(solpos['apparent_zenith'])
    pressure = pvlib.atmosphere.alt2pres(altitude)
    am_abs = pvlib.atmosphere.get_absolute_airmass(airmass, pressure)
    aoi = pvlib.irradiance.aoi(
        system['surface_tilt'],
        system['surface_azimuth'],
        solpos["apparent_zenith"],
        solpos["azimuth"],
    )
    total_irradiance = pvlib.irradiance.get_total_irradiance(
        system['surface_tilt'],
        system['surface_azimuth'],
        solpos['apparent_zenith'],
        solpos['azimuth'],
        weather['dni'],
        weather['ghi'],
        weather['dhi'],
        dni_extra=dni_extra,
        model='isotropic',
    )
    cell_temperature = pvlib.temperature.sapm_cell(
        total_irradiance['poa_global'],
        weather["temp_air"],
        weather["wind_speed"],
        **temperature_model_parameters,
    )
    effective_irradiance = pvlib.pvsystem.sapm_effective_irradiance(
        total_irradiance['poa_direct'],
        total_irradiance['poa_diffuse'],
        am_abs,
        aoi,
        module,
    )
    dc = pvlib.pvsystem.sapm(effective_irradiance, cell_temperature, module)
    ac = pvlib.inverter.sandia(dc['v_mp'], dc['p_mp'], inverter)
    annual_energy = ac.sum()
    energies[name] = annual_energy
    
    
energies = pd.Series(energies)


# based on the parameters specified above, these are in W*hrs
print(energies)
energies.plot(kind='bar', rot=0)
plt.ylabel('Yearly energy yield (W hr)')
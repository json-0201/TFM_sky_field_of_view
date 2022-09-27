# TFM_sky_field_of_view

## Brief Description

The idea for this master's final project came from investigating the PV-integrated electric vehicle.

There are many sky diffuse model for estimating the amount of solar irradiance the sun provides.
When calculating PV parameters and production, Isotropic diffuse model may not be appropriate for urban environments, where obstacles such as buildings and trees block the view of the panels (PV-integrated electric vehicles are likely to be within such environment).

A university facility's parking structures are used as a representation of an urban environment, where the sky images will be taken throughout distinct parking spot via commercially available IP camera capable of capturing the hemispheric-view.

This project will highlight the difference bewteen two diffuse model: Isotropic, SFV(sky field of view)

SFV is defined as the ratio of visible sky to the hemispheric view of the sky from the panel's perspective.
This ratio will be calculated using image-processing techniques implemented in an open-source library for Python (OpenCV).
The PV simulation will be done on Python as well, using another open-source library called PVLib.

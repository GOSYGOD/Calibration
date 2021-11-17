# Calibration upper computer

This upper computer is used for initial calibration of base station. We can't obtain 
the exact station information after installation, because the environment error will 
change at different place. Using this tool can calculate the parameters that the fusion 
software need.

The upper computer has two input way: direct input or reading file. At the same time, 
it has three calculation function: north angle, distance error, and translation params.

## Func

* North angle: Calculating the north angle of single station.
* Distance error: Calculating the distance error of detected position and real position 
based on station north angle.
* Translation params: When using two stations, there relative position need to be 
calculated. We can choose one as the main station, the other one as the secondary 
station. Our goal is moving the point cloud obtained by the secondary station to 
the main station coordinate system, so we need to translate the second's system as same 
as the main's.

## Using

Cloning the whole repository, open the project and run the "Application.py" file in main folder.

## Environment

* Python: above 3.6
* Tkinter
* numpy

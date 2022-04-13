#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# geo_coords_ex1.py
#
# Simple Example for SparkFun ublox GPS products 
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, July 2020
# 
# Do you like this library? Help support SparkFun. Buy a board!
# https://sparkfun.com
#==================================================================================
# GNU GPL License 3.0
# Copyright (c) 2020 SparkFun Electronics
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#==================================================================================
# Example 1
# This example sets up the serial port and then passes it to the UbloxGPs
# library. From here we call geo_coords() and to get longitude and latitude. I've
# also included heading of motion here as well. 

import serial

#from ublox_gps import UbloxGps
from ublox_gps.ublox_gps import UbloxGps
import time

#port = serial.Serial('/dev/serial0', baudrate=38400, timeout=1)
port = serial.Serial('/dev/ttyUSB1', baudrate=115200, timeout=1)
gps = UbloxGps(port)

print("HERE")
'''
Message UBX-NAV2-VELNED
Velocity solution in NED frame

Type Periodic/polled

Comment See important comments concerning validity of position given in section Navigation output filters in the
integration manual.

'''



'''
Message NMEA-NAV2-GGA
Global positioning system fix data
Type Output
Comment Time and position, together with GPS fixing-related data (number of satellites in use, and the resulting HDOP,
age of differential data if in use, etc.).
To identify the navigation data source for NMEA Secondary filter output, the alphanumeric string source-
identification (s:) parameter is used in a TAG Block, in respect to NMEA 0183 Standard.
☞ The output of this message is dependent on the currently selected datum (default: WGS84). The NMEA
specification indicates that the GGA message is GPS-specific. However, when the receiver is configured for
multi-GNSS, the GGA message contents will be generated from the multi-GNSS solution. For multi-GNSS
use, it is recommended that the NMEA-GNS message is used instead.
'''

'''
.9.2.2 Lat/Long position data
Message NMEA-PUBX-POSITION
Lat/Long position data
'''


time.sleep(3)

print("Listening for UBX Messages")
while True: 
    #GPS LAT LON  heading of motion    +  GPS UTC Date time
    #The payload of the NAV Class and PVT Message ID
    geo = gps.geo_coords()
    print("Longitude: ", geo.lon) 
    print("Latitude: ", geo.lat)
    print("Height (above ellipsoid): ", geo.height)
    print("Height (above mean sea level): ",geo.hMSL)

    print("Accuracy error estimate (Horizontial) [mm]:",geo.hAcc)
    print("Accuracy error estimate (Vertical) [mm]:",geo.vAcc)

    print("NED north velocity [mm/s]",geo.velN)
    print("NED east  velocity [mm/s]",geo.velE)
    print("NED down  velocity [mm/s]",geo.velD)
    
    print("Ground speed 2D [mm/s]",geo.gSpeed)            
    print("Heading of Motion: ", geo.headMot)

    print("Position pDOP:",geo.pDOP)

    print(" Number of satellites used to get position =>"+str(geo.numSV))

    print("="*30)

    gps_time = geo#gps.date_time()
    print("{}/{}/{}".format(gps_time.day, gps_time.month, gps_time.year))
    print("UTC Time {}:{}:{}".format(gps_time.hour, gps_time.min, gps_time.sec))
    print("Valid date:{}\nValid Time:{}".format(gps_time.valid.validDate, gps_time.valid.validTime))


    print("="*30)
    gps_msg_valid_status = geo
    print(gps_msg_valid_status.valid)

    print("="*30)

    gps_status = geo

    #print("Last correction time =>"+str(gps_status.flags3.lastCorrectionAge))
    print("fixType (GPS health) =>"+str(gps_status.fixType))
    print("fix status - valid fix? =>"+str(gps_status.flags.gnssFixOK))
    print("fix status - differential correction used? =>"+str(gps_status.flags.diffSoln))
    print("fix status - power mode =>"+str(gps_status.flags.psmState))
    print("fix status - heading valid? =>"+str(gps_status.flags.headVehValid))


port.close()




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

from ublox_gps import UbloxGps

#port = serial.Serial('/dev/serial0', baudrate=38400, timeout=1)
port = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)
gps = UbloxGps(port)



try:
    print("Listening for UBX Messages")
    while True:
        try: 
            #GPS LAT LON  heading of motion    +  GPS UTC Date time
            #The payload of the NAV Class and PVT Message ID
            geo = gps.geo_coords()
            print("Longitude: ", geo.lon) 
            print("Latitude: ", geo.lat)
            print("Heading of Motion: ", geo.headMot)

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
            
            #global sat_info
            #sat_info = gps.satellites()
            #print(sat_info)
            
        except (ValueError, IOError) as err:
            print(err)

finally:
    port.close()




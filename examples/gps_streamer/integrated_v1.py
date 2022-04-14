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

import utm  #lat lon converter

import struct
import sys
import socket
import time

#####################
#Create template structure for the GPSData first.
data=[None]*18
data[0] = struct.pack("=B", 17 )  #MAGIC number
data[1] = struct.pack("=B", 0 )   # 0
data[2] = struct.pack("=B", 250)  #GPSData type enum
data[3] = struct.pack("=B", 0 )   # 0
data[4] = struct.pack("=B", 0)  #source  # old value = 5 
data[5] = struct.pack("=B", 1  )  #version
data[6] = struct.pack("=B", 0  )  # m_length,(just message length?)  first part of uint16_t
data[7] = struct.pack("=B", 0 )  # m_length,(just message length?)  second part of uint16_t

data[8]   = struct.pack("d", 1234)   #timestamp      d= 8    #either this or pos X Y crashed 
data[9]   = struct.pack("=B", 0 )    #type             1
data[10]  = struct.pack("=B", 5 )    #fix               1
data[11]  = struct.pack("d", 5000)    #position_x     d= 8
data[12]  = struct.pack("d", 5010)   #position_y         d= 8
data[13]  = struct.pack("=B", 10 )   #UTMzone               1
data[14]  = struct.pack("=B", 99 )   #UTMLetter  #char?     1
data[15]  = struct.pack("d", 20 )   #Altitude             d=8
data[16]  = struct.pack("f", 77 )   #HDOP                f =4
data[17]  = struct.pack("=B", 9  )   #satellites           1
#######################

#on QCHD, open GPS serial port to get GPS data
port = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
gps = UbloxGps(port)

#on QCHD, open socket to send out QCHD GPSData format
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
client_socket.settimeout(1.0)
addr = ("127.0.0.1", 1603)

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
    print("GPS Timestamp :"+str(gps_time.iTOW))


    print("="*30)
    gps_msg_valid_status = geo
    print(gps_msg_valid_status.valid)

    print("="*30)

    gps_status = geo
    try:
        print("Last correction time =>"+str(gps_status.flags3.lastCorrectionAge))
    except AttributeError:
        print("Last correction time => NULL (probably no RTK yet)")
        
    print("fix status - RTK status [1=float, 2=fixed] =>"+str(gps_status.flags.carrSoln)) #0 1 float 2 fix        
    print("fixType (GPS health) =>"+str(gps_status.fixType))
    print("fix status - valid fix? =>"+str(gps_status.flags.gnssFixOK))
    print("fix status - differential correction used? =>"+str(gps_status.flags.diffSoln))
    print("fix status - power mode =>"+str(gps_status.flags.psmState))
    print("fix status - heading valid? =>"+str(gps_status.flags.headVehValid))

    #Lat Lon to UTM
    utm_x, utm_y,utm_zone,utm_letter=utm.from_latlon(geo.lat, geo.lon)

    #shove everything in
    #Timestamp,  iTOW seems to be unix timestamp, since it starts from 1 1 1980, weird that it does not say it is unix-timestamp directly...
    data[8]   = struct.pack("d", gps_time.iTOW)
    #Fix
    data[10]  = struct.pack("=B", gps_status.fixType )
    #UTM X
    data[11]  = struct.pack("d", utm_x)
    #UTM Y
    data[12]  = struct.pack("d", utm_y)
    #UTM ZONE
    data[13]  = struct.pack("=B", utm_zone )   #decode by ascii table to get num
    #UTM letter
    data[14]  = struct.pack("=B", ord(utm_letter) )
    #Altitude
    data[15]  = struct.pack("d", geo.hMSL )  #changed to use mean sea level, due to tradition
    #HDOP
    data[16]  = struct.pack("f", geo.pDOP )
    #satellites
    data[17]  = struct.pack("=B", geo.numSV  )    #decode by ascii table to get num
    

    #1 1234 timestamp
    #2 0 unkown
    #3 5 fix
    #4 5000 pos_x
    #5 5010 pos_y
    #6 c    #UTMLetter still need verify value tho
    #7 0
    #8 xsfesgheslvgfhaelfheslg
    #9 20    #Altitude
    #10 77   #HDop

    #send GPSData format data
    message = b''.join(data)
    client_socket.sendto(message, addr)

    time.sleep(0.1)


port.close()




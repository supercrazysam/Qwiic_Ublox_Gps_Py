#!/usr/bin/env python3

import serial

#from ublox_gps import UbloxGps
from ublox_gps.ublox_gps import UbloxGps

import utm  #lat lon converter

import struct
import sys
import socket
import time
import os

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
data[9]   = struct.pack("=B", 0 )    #type             1



#=======================================#
#Port initialization
#=======================================#
#on QCHD, open GPS serial port to get GPS data
port = serial.Serial('/dev/ttyS2', baudrate=115200, timeout=1)
gps = UbloxGps(port)

#on QCHD, open socket to send out QCHD GPSData format
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
client_socket.settimeout(1.0)
addr = ("127.0.0.1", 1603)    #GPS 1603   

#interact with FPGA internal time  (it is a linux device)
fpga_internal_time_server = os.open("/dev/pps_time", os.O_RDWR)

print("Listening for UBX Messages")
while True: 
    #GPS LAT LON  heading of motion    +  GPS UTC Date time
    #The payload of the NAV Class and PVT Message ID
    gps_pvt_msg = gps.geo_coords()

    #============================================#
    #FPGA Time processing/compare/update starts
    #============================================#
    #receive FPGA time now
    fpga_internal_time = os.read(fpga_internal_time_server,8) #read 8 bytes, first 4 bytes seconds,   the other 4 bytes microseconds
    fpga_internal_time_sec      = struct.unpack("I",fpga_internal_time[:4])
    fpga_internal_time_microsec = struct.unpack("I",fpga_internal_time[4:])

    #check if local GPS time is valid, if not valid "continue" and skip the rest               (To be implementedL: Also if the fix is float or fixed)
    if ((gps_pvt_msg.valid.fullyResolved & gps_pvt_msg.valid.validDate & gps_pvt_msg.valid.validTime)==0):
        pass
    else:
        #compare with local GPS time
        #if "seconds" part of local GPS time, is different than remote FPGA time,  assemble packet and send out,
        local_gps_time = int(gps_pvt_msg.iTOW/1000)  #local gps time in seconds

        if local_gps_time != fpga_internal_time_sec:
            os.write(fpga_internal_time_server, struct.pack("I", local_gps_time))   #I is not enough?  struct.error: 'I' format requires 0 <= number <= 4294967295
        
    #============================#
    #Assemble GPSData
    #============================#
    #Lat Lon to UTM
    utm_x, utm_y,utm_zone,utm_letter=utm.from_latlon(gps_pvt_msg.lat, gps_pvt_msg.lon)

    #shove everything in
    #Timestamp,  iTOW seems to be unix timestamp, since it starts from 1 1 1980, weird that it does not say it is unix-timestamp directly...
    data[8]   = struct.pack("d", gps_pvt_msg.iTOW)
    #Fix
    data[10]  = struct.pack("=B", gps_pvt_msg.fixType )
    #UTM X
    data[11]  = struct.pack("d", utm_x)
    #UTM Y
    data[12]  = struct.pack("d", utm_y)
    #UTM ZONE
    data[13]  = struct.pack("=B", utm_zone )   #decode by ascii table to get num
    #UTM letter
    data[14]  = struct.pack("=B", ord(utm_letter) )
    #Altitude
    data[15]  = struct.pack("d", gps_pvt_msg.hMSL )  #changed to use mean sea level, due to tradition
    #HDOP
    data[16]  = struct.pack("f", gps_pvt_msg.pDOP )
    #satellites
    data[17]  = struct.pack("=B", gps_pvt_msg.numSV  )    #decode by ascii table to get num

    #send GPSData format data
    message = b''.join(data)
    client_socket.sendto(message, addr)

    #===================================#
    #print part
    #===================================#
    print("Longitude: ", gps_pvt_msg.lon) 
    print("Latitude: ", gps_pvt_msg.lat)
    print("Height (above ellipsoid): ", gps_pvt_msg.height)
    print("Height (above mean sea level): ",gps_pvt_msg.hMSL)

    print("Accuracy error estimate (Horizontial) [mm]:",gps_pvt_msg.hAcc)
    print("Accuracy error estimate (Vertical) [mm]:",gps_pvt_msg.vAcc)

    print("NED north velocity [mm/s]",gps_pvt_msg.velN)
    print("NED east  velocity [mm/s]",gps_pvt_msg.velE)
    print("NED down  velocity [mm/s]",gps_pvt_msg.velD)
    
    print("Ground speed 2D [mm/s]",gps_pvt_msg.gSpeed)            
    print("Heading of Motion: ", gps_pvt_msg.headMot)

    print("Position pDOP:",gps_pvt_msg.pDOP)

    print(" Number of satellites used to get position =>"+str(gps_pvt_msg.numSV))

    print("="*30)

    print("{}/{}/{}".format(gps_pvt_msg.day, gps_pvt_msg.month, gps_pvt_msg.year))
    print("UTC Time {}:{}:{}".format(gps_pvt_msg.hour, gps_pvt_msg.min, gps_pvt_msg.sec))
    print("Valid date:{}\nValid Time:{}".format(gps_pvt_msg.valid.validDate, gps_pvt_msg.valid.validTime))
    print("GPS Timestamp :"+str(gps_pvt_msg.iTOW))


    print("="*30)
    print(gps_pvt_msg.valid)
    print("="*30)

    try:
        print("Last correction time =>"+str(gps_pvt_msg.flags3.lastCorrectionAge))
    except AttributeError:
        print("Last correction time => NULL (probably no RTK yet)")
        
    print("fix status - RTK status [1=float, 2=fixed] =>"+str(gps_pvt_msg.flags.carrSoln)) #0 1 float 2 fix        
    print("fixType (GPS health) =>"+str(gps_pvt_msg.fixType))
    print("fix status - valid fix? =>"+str(gps_pvt_msg.flags.gnssFixOK))
    print("fix status - differential correction used? =>"+str(gps_pvt_msg.flags.diffSoln))
    print("fix status - power mode =>"+str(gps_pvt_msg.flags.psmState))
    print("fix status - heading valid? =>"+str(gps_pvt_msg.flags.headVehValid))

    
#exit cleanup
port.close()
os.close(fpga_internal_time_server)



#!/usr/bin/env python3
import struct
import sys
import socket
import time

#####################
#Create template structure for the GPSData first.
##data=[None]*18
##data[0] = struct.pack("=B", 17 )  #MAGIC number
##data[1] = struct.pack("=B", 0 )   # 0
##data[2] = struct.pack("=B", 250)  #GPSData type enum
##data[3] = struct.pack("=B", 0 )   # 0
##data[4] = struct.pack("=B", 0)  #source  # old value = 5 
##data[5] = struct.pack("=B", 1  )  #version
##data[6] = struct.pack("=B", 0  )  # m_length,(just message length?)  first part of uint16_t
##data[7] = struct.pack("=B", 0 )  # m_length,(just message length?)  second part of uint16_t
##
##data[8]   = struct.pack("d", 1234)   #timestamp      d= 8    #either this or pos X Y crashed 
##data[9]   = struct.pack("=B", 0 )    #type             1
##data[10]  = struct.pack("=B", 5 )    #fix               1
##data[11]  = struct.pack("d", 5000)    #position_x     d= 8
##data[12]  = struct.pack("d", 5010)   #position_y         d= 8
##data[13]  = struct.pack("=B", 10 )   #UTMzone               1
##data[14]  = struct.pack("=B", 99 )   #UTMLetter  #char?     1
##data[15]  = struct.pack("d", 20 )   #Altitude             d=8
##data[16]  = struct.pack("f", 77 )   #HDOP                f =4
##data[17]  = struct.pack("=B", 9  )   #satellites           1
#######################


'''
>>> value
b"\x15'\x00\x00lB\x00\x00"
>>> value_a
b"\x15'\x00\x00"
>>> value_b
b'lB\x00\x00'
'''

#==== Tested QCHD onboard, it works
import os
import struct

f = os.open("/dev/pps_time", os.O_RDWR)
value = os.read(f,8)

value_a = value[:4]
value_b = value[4:]

struct.unpack("I",value_a)

#==========
os.write(f, struct.pack("I", 1000))   #setter




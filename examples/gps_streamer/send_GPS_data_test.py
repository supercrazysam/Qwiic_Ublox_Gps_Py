#!/usr/bin/env python3

import struct
import sys
import socket

'''

MAGIC_NUMBER = 18

==========
/** 
  * @brief Enumerates the message types
  * 
  */
typedef enum {
   STEREO_CALIBRATION_MSG      = 210, /*!< Stereo calibration message */
   IMU_CALIBRATION_MSG         = 211, /*!< Imu calibration message */
   IMAGE_STREAM_METADATA_MSG   = 240, /*!< Streams metadata */
   CAMERA_SETTINGS_MSG         = 241, /*!< Camera settings */
   SIGNAL_MSG                  = 242, /*!< System signal message */
   SYSTEM_PARAMETERS_MSG       = 243, /*!< System parameters */
   TIME_SYNC_MSG               = 244, /*!< Time sync message */
   CAMERA_POSE_MSG             = 245, /*!< Camera position message */
   VISODO_LANDMARKS_MSG        = 246, /*!< Visual odometry landmark message */
   XSENS_DATA_MSG              = 247, /*!< XSens sensor data */
   VISODO_STATUS_MSG           = 248, /*!< Visual odometry status */
   AUTO_EXPOSURE_SETTINGS_MSG  = 249, /*!< Autoexposure daemon settigns */
   AUTO_EXPOSURE_SETTINGS2_MSG = 208, /*!< Autoexposure daemon settigns */
   GPS_DATA_MSG                = 250, /*!< GPS sensor data */
   VISODO_INPUT_MSG            = 251, /*!< TODO: Ask JP */
   VISODO_INPUT_RETURN_MSG     = 252, /*!< TODO: Ask JP */
   VISODO_LOOP_CLOSURE_MSG     = 253, /*!< Visodo loop closure */
   AUTO_EXPOSURE_CONTROL_MSG   = 209  /*!< Autoexposure daemon control */
} MessageType;




==========
Header::Header(uint8_t type, uint8_t version, uint16_t length, uint8_t source, uint32_t hwrev)

Header::Header() : m_type(0), m_version(0), m_length(0), m_source(0)


int Header::serialize(char* buffer)
{
   buffer[0] = MAGIC_NUMBER;
   buffer[1] = 0;
   buffer[2] = m_type;
   buffer[3] = 0;
   buffer[4] = m_source;
   buffer[5] = m_version;
   buffer[6] = m_length >> 8;
   buffer[7] = m_length & 0xff;
   int bytesRead = 8;
   bytesRead += set_uint4((uint8_t*)&(buffer[bytesRead]), m_hwrev);

   return bytesRead;
}


==========
typedef enum {
  UTM=0,
  LATLONG
} GPSType;



=====================================
  //timestamp
  double timestamp;
  
  GPSType type;

  uint8_t fix;
  //UTM
  double x;
  double y;
  uint8_t UTMzone;
  char    UTMletter; 
  
  //LAT/LONG
  double latitude; //north > 0 , South < 0
  double longitude; //east > 0, west < 0
  
  double altitude; //DBL_MAX if not available
  
  float hdop;  //horizontal dilution of precision. A measure of the geometric quality of a GPS satellite configuration in the sky. HDOP is a factor in determining the relative accuracy of a horizontal position. The smaller the DOP number, the better the geometry.
  uint8_t satellites;
'''

''''
//---------------------------------------------------------------------------------------------------
int set_double(uint8_t* buf, double v)
{
  memcpy(buf, (char*)&v, sizeof(double));

  return sizeof(double);
}

//---------------------------------------------------------------------------------------------------
int set_float(uint8_t* buf, float v)
{
  memcpy(buf, (char*)&v, sizeof(float));

  return sizeof(float);
}



''''



#GPS  (total length 11 byte)

# 1 byte header
#

# 10 byte data
#     1) set_double  => timestamp
#     2) (int? uint8_t?) 0 for UTM   => type of GPS,  0 if UTM, 1 if LATLONG
#     3) (uint8_t) num_of_fix (quality? maybe)  => fix
#     4) set_double  => position_x
#     5) set_double  => position_y
#     6) (uint8_t) UTMzone
#     7) (uint8_t) UTMLetter   (char???)
#     8) set_double => altitude
#     9) set_float => HDOP
#     10) (uint8_t) satellites




sys.exit(0)





#example UDP client sender
for pings in range(10):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
    client_socket.settimeout(1.0)
    message = b'test'
    addr = ("127.0.0.1", 12000)

    start = time.time()
    client_socket.sendto(message, addr)
    try:
        data, server = client_socket.recvfrom(1024)
        end = time.time()
        elapsed = end - start
        print(f'{data} {pings} {elapsed}')
    except socket.timeout:
        print('REQUEST TIMED OUT')


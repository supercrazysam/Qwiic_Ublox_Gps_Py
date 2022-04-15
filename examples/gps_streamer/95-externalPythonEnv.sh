#!/bin/sh


#screen -S "GPS" -dm bash -rc "python3"


screen -S "GPS" -dm bash -c "export PYTHONPATH=$PYTHONPATH:/nrec/python_pkgs;python3 /nrec/pyserial/gps/Qwiic_Ublox_Gps_Py/examples/gps_streamer/integrated_v1.py"


#!/usr/bin/env python3
##########################################
# Parser for output data from Aidon energy meter
# with RJ45 HAN connector (Norwegian style)
# used by Skellefteå Kraft
#
# Based on dlms_cosem examples.
# Olov Lindström
# 220423
##########################################
from dlms_cosem.protocol import xdlms
from dlms_cosem.hdlc import frames
from dlms_cosem.utils import parse_as_dlms_data
from dlms_cosem.cosem import Obis
from dlms_cosem.time import datetime_from_bytes


units = { 
    27:'W',
    29:'VA(r)',
    33:'A',
    35:'V',
    30:'Wh',
    32:'VAh(r)'
    }

def parse(hdlc_data):
    retval={}
    
    ui = frames.UnnumberedInformationFrame.from_bytes(hdlc_data)

    dn = xdlms.DataNotification.from_bytes(
        ui.payload[3:]
    )  # The first 3 bytes should be ignored.
    result = parse_as_dlms_data(dn.body)

    for item in result:
        obis = Obis.from_bytes(item[0])
        if obis == Obis(a=0, b=0, c=1, d=0, e=0, f=255):
            # clock
            clock, stats = datetime_from_bytes(item[1])
            retval[obis.to_string()]={'value':clock,'unit':''}
        elif len(item)==3:
            desc=item[2]
            if desc[1] in [33,35]:
                value = round(float(item[1])*10.0**(desc[0]),2)
            else:
                value = item[1]
            if desc[1] in units:
                unit=units[desc[1]]
            else:
                unit='NA'
            retval[obis.to_string()]={'value':value,'unit':unit}
        else:
            print(f"Dont know how to handle obis {obis.to_string()}")

    return retval

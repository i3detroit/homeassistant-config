#!/usr/bin/env python
# -*- coding: utf-8 -*-

import appdaemon.appapi as appapi
import socket
import datetime
from influxdb import InfluxDBClient

class CheckPowerMeter(appapi.AppDaemon):
    def initialize(self):
        time = datetime.time(0, 0, 0)
        self.run_daily(self.do_the_thing, time)

    def do_the_thing(self, kwargs):
        pm = PowerMeter()
        pm.connect()
        while True:
            packet = pm.update()
            if packet is not None:
                client = InfluxDBClient('localhost', 8086, 'hass', 'hass', 'hass')
                result = client.query("select value from \"kWh\" WHERE entity_id='i3_power_meter' AND time < now() - 1437m and time > now() - 1443m;")
                try:
                    yesterdayPower = list(result.get_points('kWh'))[0]['value']
                    powerDiff = str(round(packet['total_kWh'] - yesterdayPower, 1))
                    msgString = 'Power meter is ' + str(packet['total_kWh']) + 'kWh which is ' + powerDiff + ' kWh more than 24 hours ago'
                    self.call_service("notify/slack_statusbots", message = msgString)
                    break
                except IndexError:
                    msgString = 'Power meter is ' + str(packet['total_kWh']) + 'kWh. Error retrieving yesterday\'s power useage.'
                    self.call_service("notify/slack_statusbots", message = msgString)
                    break
        pm.close()

class PowerMeter():
    '''Define methods to talk with an EKM power meter over socket'''
    
    # RocketPort Ethernet <-> RS-485 device
    HOST = '10.13.0.20'
    PORT = 8000

    # string to send to ask the meter for a reading
    QUERY = '/?000010000863\r\n'

    # string to close a communicaiton with the meter
    CLOSE = '\x01B0\x03u'

    # EKM-published CRC16 table
    CRC_LOOKUP = [
            0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
            0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
            0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
            0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
            0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
            0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
            0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
            0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
            0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
            0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
            0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
            0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
            0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
            0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
            0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
            0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
            0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
            0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
            0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
            0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
            0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
            0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
            0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
            0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
            0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
            0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
            0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
            0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
            0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
            0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
            0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
            0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040
        ]

    def __init__(self):
        self.connection = None

    def connect(self):
        '''Set up a blocking socket with a timeout'''
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((self.HOST,self.PORT))
        self.connection.settimeout(30)
    
    def calc_crc16(self,packet):
        '''Compute the EKM-published CRC16 for a packet'''
        test = [ord(c) for c in packet['data']]
        
        crc = 0xFFFF
        for c in test:
            crc = ((crc >> 8) & 0xFF) ^ self.CRC_LOOKUP[(crc ^ c) & 0xFF]
        
        swapped = ((crc << 8) | (crc >> 8)) & 0xFFFF
        return swapped & 0x7F7F
        
    def isvalid(self,packet):
        '''Determine if the packet is valid using the CRC16'''
        return packet['crc'] == self.calc_crc16(packet)
        
    def update(self):
        '''Ask for a reading'''
        self.connection.sendall(self.QUERY.encode('utf-8'))

        # The RocketPort seems to be slow about sending all the data at once,
        # so spin until we have the whole 255-byte packet
        raw = ''
        while len(raw) < 255:
            raw += self.connection.recv(255).decode('utf-8')
        
        # hand off the parsed packet
        return self.parse(raw)
        
    def parse(self,raw):
        '''Parse a data packet from an EKM power meter'''
        try:
            # comments on lines are expected values if parsing the example
            # packet in the EKM official communications document
            
            # offsets calculated by hand from that document until things aligned
            packet = {
                'model':              raw[0x01:0x03],           # '\x10\x17'
                'fw_version':     ord(raw[0x03]),               #   19
                'address':        int(raw[0x04:0x10]),          #10015
                'total_kWh':    float(raw[0x10:0x18])/10,       # 3056.3
                't1_kWh':       float(raw[0x18:0x20])/10,       # 1437.4
                't2_kWh':       float(raw[0x20:0x28])/10,       #  831.2
                't3_kWh':       float(raw[0x28:0x30])/10,       #  321.2
                't4_kWh':       float(raw[0x30:0x38])/10,       #  466.5
                'total_rev_kWh':float(raw[0x38:0x40])/10,       #    0.0
                't1_rev_kWh':   float(raw[0x40:0x48])/10,       #    0.0
                't2_rev_kWh':   float(raw[0x48:0x50])/10,       #    0.0
                't3_rev_kWh':   float(raw[0x50:0x58])/10,       #    0.0
                't4_rev_kWh':   float(raw[0x58:0x60])/10,       #    0.0
                'voltage1':     float(raw[0x60:0x64])/10,       #  118.8
                'voltage2':     float(raw[0x64:0x68])/10,       #  118.9
                'voltage3':     float(raw[0x68:0x6C])/10,       #  120.8
                'current1':     float(raw[0x6C:0x71])/10,       #   18.0
                'current2':     float(raw[0x71:0x76])/10,       #   18.0
                'current3':     float(raw[0x76:0x7B])/10,       #    1.0
                'power1':         int(raw[0x7B:0x82]),          # 2050
                'power2':         int(raw[0x82:0x89]),          # 2050
                'power3':         int(raw[0x89:0x90]),          #  160
                'total_power':    int(raw[0x90:0x97]),          # 4270
                'cos1':         float(raw[0x98:0x9B])/100,      #    1.00
                'cos2':         float(raw[0x9C:0x9F])/100,      #    1.00
                'cos3':         float(raw[0xA0:0xA3])/100,      #    0.83
                'max_demand':   float(raw[0xA3:0xAB])/10,       #14275.0
                'demand_period':  int(raw[0xAB]),               #    1
                'timestamp':datetime.datetime.strptime(
                                      raw[0xAC:0xB2]+           #'110217' => 2011-02-17
                                      raw[0xB4:0xBA],           #'114637' => 11:46:37
                                      '%y%m%d%H%M%S'),
                'CT_rating':      int(raw[0xBA:0xBE]),          # 1000
                'pulse1_count':   int(raw[0xBE:0xC6]),          #    0
                'pulse2_count':   int(raw[0xC6:0xCE]),          #    0
                'pulse3_count':   int(raw[0xCE:0xD6]),          #    0
                'pulse1_ratio':   int(raw[0xD6:0xDA]),          #    0
                'pulse2_ratio':   int(raw[0xDA:0xDE]),          #    0
                'pulse3_ratio':   int(raw[0xDE:0xE2]),          #    0
                'pulse_HL':       int(raw[0xE2:0xE5]),          #    0
                'reserved':           raw[0xE5:0xF9],           # '00000000000000000000'
                'unknown':            raw[0xF9:0xFD],           # '!\x0D\x0A\x03'
                'data':               raw[0x01:0xFD],
                'crc':           ((ord(raw[0xFD])<<8)+          # 0x77
                                  ord(raw[0xFE])) & 0xFFFF      # 0x3F
            }
            
            # if the packet passes CRC16 validation, return it
            if self.isvalid(packet):
                return packet
                
            # otherwise, the packet is worthless so return nothing
            else:
                return None
        except ValueError:
            # maybe a bad character or other corruption in the packet; do nothing
            return None
    
    def close(self):
        '''Close the connection to the power meter'''
        self.connection.send(self.CLOSE.encode('utf-8'))
        self.connection.close()

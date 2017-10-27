#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import Adafruit_MCP3008
import math

CLK  = 18
MISO = 23
MOSI = 24
CS   = 25

parser = argparse.ArgumentParser(description='Script to read AC current values from ACS712 via MCP3008.',version="0.1")
parser.add_argument('-c', action="store", default="0", dest="channel",help='ADC channel to read. Starting from 0.',type=int)
results = parser.parse_args()
channel = results.channel

mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
value = 0
print "Reading 50000 samples"
for i in range(50000):
  print "Reading sample " + str(i)
  value = value + mcp.read_adc(channel)
avg = value / 50000
print math.sqrt(avg)
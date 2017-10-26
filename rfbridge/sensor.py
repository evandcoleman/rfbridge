#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading
import time
import Adafruit_MCP3008

from threading import Thread

_logger = logging.getLogger(__name__)
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25

class Sensor(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

    def run(self):
        while True:
            self.read_sensors()
            time.sleep(2)

    def set_callback(self, callback):
        self.callback = callback

    def read_sensors(self):
        _logger.info("Reading sensors...")
        # Read all the ADC channel values in a list.
        values = [0]*8
        for i in range(8):
            # The read_adc function will get the value of the specified channel (0-7).
            values[i] = self.mcp.read_adc(i)
        # Print the ADC values.
        self.callback('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
        # Pause for half a second.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from rflib import *

_logger = logging.getLogger(__name__)

class Transmitter:

    def __init__(self, frequency, baudRate):
        self.d = RfCat()
        self.d.setFreq(frequency)
        self.d.setMdmModulation(MOD_ASK_OOK)
        self.d.setMdmDRate(baudRate)
        self.d.makePktFLEN(0)
        self.d.lowball(0)
        self.d.setMdmChanSpc(24000)
        self.d.setChannel(0)
        self.d.setMaxPower()

    def xmit(self, cmd, times=10):
        self.d.RFxmit(cmd * times)

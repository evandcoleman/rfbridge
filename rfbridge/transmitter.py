#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from rflib import *

_logger = logging.getLogger(__name__)

class Transmitter:

    def __init__(self, config):
        self.config = config
        self.commands = config.commands
        self.d = RfCat()
        self.d.setFreq(config.frequency)
        self.d.setMdmModulation(MOD_ASK_OOK)
        self.d.setMdmDRate(config.baud_rate)
        self.d.makePktFLEN(0)
        self.d.lowball(0)
        self.d.setMdmChanSpc(24000)
        self.d.setChannel(0)
        self.d.setMaxPower()

    def xmit(self, cmd, times=10):
        self.d.RFxmit(self.commands[cmd] * times)

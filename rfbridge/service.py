#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import socket

from zeroconf import ServiceInfo, Zeroconf

_logger = logging.getLogger(__name__)

class Service:

    def __init__(self):
        self.name = name
        self.zeroconf = Zeroconf()

    def advertise(self):
        hostname, port = get_open_port()
        desc = {'service': 'RF Bridge', 'version': '1.0.0'}
        info = ServiceInfo(
            "_rfbridge._tcp.local.",
            self.name + "._rfbridge._tcp.local.",
            socket.inet_aton("127.0.0.1"), port, 0, 0,
            desc, hostname + ".local."
        )
        self.zeroconf.register_service(info)

    def get_open_hostname_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("",0))
        hostname = socket.gethostname()
        port = s.getsockname()[1]
        s.close()
        return hostname, port

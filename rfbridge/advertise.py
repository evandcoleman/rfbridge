#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import socket

from zeroconf import ServiceInfo, Zeroconf

_logger = logging.getLogger(__name__)

class Advertise:

    def __init__(self):
        self.zeroconf = Zeroconf()

    def get_hostname_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("",0))
        hostname = socket.gethostname()
        port = s.getsockname()[1]
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return hostname, port

    def start(self):
        hostname, port = self.get_hostname_port()
        self.port = port
        desc = {'service': 'RF Bridge', 'version': '0.0.1'}
        info = ServiceInfo(
            "_rfbridge._tcp.local.",
            hostname + "._rfbridge._tcp.local.",
            socket.gethostbyname(socket.gethostname()), port, 0, 0,
            desc, hostname + ".local."
        )
        self.zeroconf.register_service(info)

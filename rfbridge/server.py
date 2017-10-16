#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import socket

from websocket_server import WebsocketServer

_logger = logging.getLogger(__name__)

class Server:

    def __init__(self, port):
        self.server = WebsocketServer(port, host=socket.gethostname())
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()

    def message_received(self, client, server, message):
        __logger.info(message)

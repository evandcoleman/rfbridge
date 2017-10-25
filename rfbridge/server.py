#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import socket

from websocket_server import WebsocketServer

_logger = logging.getLogger(__name__)

class Server:

    def __init__(self, port):
        self.server = WebsocketServer(port, host="0.0.0.0")
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()

    def new_client(self, client, server):
        _logger.info(client)

    def message_received(self, client, server, message):
        _logger.info(message)

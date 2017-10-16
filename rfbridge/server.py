#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from websocket_server import WebsocketServer

_logger = logging.getLogger(__name__)

class Server:

    def __init__(self, port):
        self.server = WebsocketServer(port, host='127.0.0.1', loglevel=logging.INFO)
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()

    def message_received(self, client, server, message):
        server.send_message_to_all("Hey all, a new client has joined us")

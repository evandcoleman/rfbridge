#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import socket
import threading

from websocket_server import WebsocketServer

_logger = logging.getLogger(__name__)

class Server:

    def __init__(self, port, sensor):
        self.server = WebsocketServer(port, host="0.0.0.0")
        self.server.set_fn_message_received(self.message_received)
        self.sensor = sensor
        self.sensor.set_fn_light_changed(self.light_changed)
        self.sensor.set_fn_motor_changed(self.motor_changed)
    
    def start(self):
        threading.Thread(target=self.sensor.start).run()
        self.server.run_forever()

    def new_client(self, client, server):
        _logger.info("Client connected")
        try:
            self.send_status()

    def message_received(self, client, server, message):
        _logger.info(message)

    def send_message(self, message):
        self.server.send_message_to_all(message.as_json())

    def send_status(self):
        self.send_message(Message('status', self.last_status.as_json()))

    def light_changed(self, status):
        self.last_status = status
        self.send_status()

    def motor_changed(self, status):
        self.last_status = status
        self.send_status()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading
from concurrent import futures
import grpc
from protos import rfbridge_pb2, rfbridge_pb2_grpc

_logger = logging.getLogger(__name__)

class Server(rfbridge_pb2_grpc.RFBridgeServicer):

    def __init__(self, port, sensor, tx):
        self.port = port
        self.sensor = sensor
        self.sensor.set_fn_light_changed(self.light_changed)
        self.sensor.set_fn_motor_changed(self.motor_changed)
        self.tx = tx
    
    def start(self):
        threading.Thread(target=self.sensor.start).run()
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        rfbridge_pb2_grpc.add_RFBridgeServicer_to_server(self, self.server)
        self.server.add_insecure_port("[::]:" + str(self.port))
        self.server.start()

    def stop(self):
        self.server.stop(0)

    def SendCommand(self, request, context):
        response = rfbridge_pb2.CommandResponse()

        name = CommandRequest.DESCRIPTOR.enums_by_name['command'].enum_type.values_by_number[request.command].name
        self.tx.xmit(cmd=name)

        return response

    def light_changed(self, status):
        self.last_status = status
        # self.send_status()

    def motor_changed(self, status):
        self.last_status = status
        # self.send_status()

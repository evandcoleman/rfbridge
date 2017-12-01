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

        if request.command == rfbridge_pb2.Command.Value("LIGHT"):
            self.tx.xmit(cmd="light")
        elif request.command == rfbridge_pb2.Command.Value("STOP"):
            self.tx.xmit(cmd="stop")
        elif request.command == rfbridge_pb2.Command.Value("SLOW"):
            self.tx.xmit(cmd="slow")
        elif request.command == rfbridge_pb2.Command.Value("MEDIUM"):
            self.tx.xmit(cmd="medium")
        elif request.command == rfbridge_pb2.Command.Value("FAST"):
            self.tx.xmit(cmd="fast")
        elif request.command == rfbridge_pb2.Command.Value("REVERSE"):
            self.tx.xmit(cmd="reverse")

        return response

    def light_changed(self, status):
        self.last_status = status
        # self.send_status()

    def motor_changed(self, status):
        self.last_status = status
        # self.send_status()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging
import time

from rfbridge import __version__
from rfbridge.advertise import Advertise
from rfbridge.transmitter import Transmitter
from rfbridge.server import Server
from rfbridge.sensor import Sensor
from rfbridge.devices import devices
from rfbridge.protos import rfbridge_pb2, rfbridge_pb2_grpc

__author__ = "Evan Coleman"
__copyright__ = "Evan Coleman"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Bridge RF commands to a ceiling fan with an ACS712 and Yardstick ONE")
    parser.add_argument(
        '--device',
        action="store",
        dest="device_id",
        help='The identifier of the device to bridge',
        type=str
    )
    parser.add_argument(
        '--command',
        action="store",
        dest="command",
        help='The command to send',
        type=str
    )
    parser.add_argument(
        '--bridge',
        action="store",
        dest="bridge_name",
        help='The name of this bridge',
        type=str
    )
    parser.add_argument(
        '--version',
        action='version',
        version='rfbridge {ver}'.format(ver=__version__)
    )
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO
    )
    parser.set_defaults(bridge=False)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    device = devices.devices[args.device_id]
    tx = Transmitter(config=device)

    if args.bridge_name is not None:
        _logger.info("Advertising service...")
        advertiser = Advertise(name=args.bridge_name, device_type='fan')
        advertiser.start()
        _logger.info("Advertised at port: " + str(advertiser.port))
        server = Server(port=advertiser.port, sensor=Sensor(), tx=tx)
        server.start()
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            server.stop()
            sys.exit()
    else:
        command = args.command
        tx.xmit(cmd=command)

    _logger.info("Exiting...")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

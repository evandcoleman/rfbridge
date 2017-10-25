#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging

from rfbridge import __version__
from rfbridge.advertise import Advertise
from rfbridge.transmit import Transmitter
from rfbridge.server import Server
from rfbridge.sensor import Sensor

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
        description="Bridge RF commands to a ceiling fan with an ACS217 and Yardstick ONE")
    parser.add_argument(
        '--version',
        action='version',
        version='rfbridge {ver}'.format(ver=__version__))
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
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
    _logger.info("Advertising service...")
    
    advertiser = Advertise()
    advertiser.start()
    server = Server(port=advertiser.port)
    sensor = Sensor()
    sensor.set_callback(server.send_message)

    _logger.info("Exiting...")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

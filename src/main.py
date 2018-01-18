from receiver import TicketReceiver
from draw import TicketPrinter
from printer import TestPort, TTYPort
from api import Core
import argparse
import os
import configparser
import sys


parser = argparse.ArgumentParser()
parser.add_argument("config", help="Configuration file, such as /etc/lkprint.conf")
args = parser.parse_args()

if not os.path.isfile(args.config):
    print("Configuration file", args.config, "doesn't exist")
    sys.exit(1)

config = configparser.ConfigParser()
config.read(args.config)

port = None

printers = []

if config["Printer"]["port"] == "stdout":
    printers.append(TicketPrinter(TestPort()))
else:
    for port in config["Printer"]["port"].split(","):
        printers.append(TicketPrinter(TTYPort(port)))

core = Core(config["API"]["URL"], config["API"]["Token"])

receiver = TicketReceiver(printers, core)
receiver.start()

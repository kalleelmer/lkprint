from receiver import TicketReceiver
from draw import TicketPrinter
from printer import TestPort, TTYPort
from api import Core
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("port", help="A tty to write to or 'stdout'")
parser.add_argument("api", help="The base URL of the core API")
parser.add_argument("token", help="Authentication token to use with the API")
args = parser.parse_args()

port = None

if args.port == "stdout":
    port = TestPort()
else:
    port = TTYPort(args.port)

printer = TicketPrinter(port)

core = Core(args.api, args.token)

receiver = TicketReceiver(printer, core)
receiver.start()

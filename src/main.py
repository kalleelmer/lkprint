from receiver import TicketReceiver
from draw import TicketPrinter
from printer import TestPort, TTYPort
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("port", help="A tty to write to or 'stdout'")
parser.add_argument("queue", help="The SQS queue to read from")
args = parser.parse_args()

port = None

if args.port == "stdout":
    port = TestPort()
else:
    port = TTYPort(args.port)

printer = TicketPrinter(port)

receiver = TicketReceiver(printer)
receiver.start()

from threading import Thread
import boto3
import json
from botocore.exceptions import ClientError
from time import sleep

class TicketReceiver(Thread):
    def __init__(self, printer, core):
        Thread.__init__(self, name="TicketReceiver")
        self.printer = printer
        self.core = core
        self.params = None

    def receiveMessages(self):
        print("Listening for tickets")
        while True:
            for message in self.queue.receive_messages(WaitTimeSeconds=10):
                print("Ticket:", message.body)
                ticket = json.loads(message.body)
                self.printer.printTicket(ticket)
                message.delete()
            if self.printer.getID() != self.params["id"]:
                raise IOError("Printer ID changed")
            self.core.setAlive(self.pid)
    
    def run(self):
        while True:
            try:
                print("Looking for printer")
                self.pid = self.printer.getID()
                print("Found printer", self.pid)
                print("Retrieving printer data from Core")
                self.params = self.core.getPrinter(self.pid)
                print("Printer name is", self.params["name"])
                print("URL is", self.params["url"])
                sqs = boto3.resource("sqs")
                self.queue = sqs.Queue(self.params["url"])
                self.receiveMessages()
            except (IOError, ClientError) as e:
                print("Printer down:", e)
                sleep(10)



from threading import Thread
import json
import boto3
from botocore.exceptions import ClientError
from time import sleep

class TicketReceiver(Thread):
    def __init__(self, printers, core):
        Thread.__init__(self, name="TicketReceiver")
        self.printers = printers
        self.core = core
        self.params = None

    def receiveMessages(self):
        while True:
            print("Updating printer alive status")
            self.core.setAlive(self.params["id"])
            print("Listening for tickets")
            for message in self.queue.receive_messages(WaitTimeSeconds=5):
                print("Ticket:", message.body)
                ticket = json.loads(message.body)
                ticketStatus = self.core.getTicket(ticket["2id"])
                if ticketStatus["printed"] == 0:
                    self.printer.printTicket(ticket)
                    self.core.setTicketPrinted(self.params["id"], ticket["2id"])
                else:
                    print("Already printed, status", str(ticketStatus["printed"]))
                message.delete()
            if self.pid > 0 and self.printer.getID() != self.pid:
                raise IOError("Printer ID changed")
    
    def run(self):
        while True:
            print("Scanning", len(self.printers), "printer ports")
            for printer in self.printers:
                self.printer = printer
                try:
                    self.printer.fallback = False
                    self.pid = self.printer.getID()
                    if self.pid > 0:
                        print("Found printer", self.pid)
                        print("Retrieving printer data from Core")
                        self.params = self.core.getPrinter(self.pid)
                    print("Printer name is", self.params["name"])
                    print("URL is", self.params["url"])
                    sqs = boto3.resource("sqs")
                    self.queue = sqs.Queue(self.params["url"])
                    self.receiveMessages()
                except (IOError, ClientError, OSError) as e:
                    print("Printer", self.printer, "down:", e)
                    self.printer.close()
            sleep(10)



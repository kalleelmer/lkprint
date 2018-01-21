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
        print("Listening for tickets")
        while True:
            for message in self.queue.receive_messages(WaitTimeSeconds=10):
                print("Ticket:", message.body)
                ticket = json.loads(message.body)
                self.printer.printTicket(ticket)
                message.delete()
            if self.pid > 0 and self.printer.getID() != self.pid:
                raise IOError("Printer ID changed")
            if self.sno != None and self.printer.getSerialNumber() != self.sno:
                raise IOError("Printer serial number changed")
            self.core.setAlive(self.params["id"])
    
    def run(self):
        while True:
            print("Scanning", len(self.printers), "printer ports")
            for printer in self.printers:
                self.printer = printer
                try:
                    self.pid = self.printer.getID()
                    self.sno = self.printer.getSerialNumber()
                    if self.pid > 0:
                        print("Found printer", self.pid)
                        print("Retrieving printer data from Core")
                        self.params = self.core.getPrinter(self.pid)
                    elif self.sno != None:
                        print("Found printer", self.sno)
                        print("Retrieving printer data from Core")
                        self.params = self.core.getPrinterBySerialNumber(self.sno)
                    print("Printer name is", self.params["name"])
                    print("URL is", self.params["url"])
                    sqs = boto3.resource("sqs")
                    self.queue = sqs.Queue(self.params["url"])
                    self.receiveMessages()
                except (IOError, ClientError) as e:
                    print("Printer", self.printer, "down:", e)
                    self.printer.close()
            sleep(10)



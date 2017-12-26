from threading import Thread
import boto3
import json

class TicketReceiver(Thread):
    def __init__(self, printer):
        Thread.__init__(self, name="TicketReceiver")
        self.printer = printer

    def receiveMessages(self):
        while True:
            for message in self.queue.receive_messages(WaitTimeSeconds=10):
                print("Ticket:", message.body)
                ticket = json.loads(message.body)
                self.printer.printTicket(ticket)
                message.delete()
    
    def run(self):
        sqs = boto3.resource("sqs")
        self.queue = sqs.get_queue_by_name(QueueName="print-dev-1")
        self.receiveMessages()



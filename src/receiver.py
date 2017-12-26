from threading import Thread
import boto3

class TicketReceiver(Thread):
    def __init__(self):
        Thread.__init__(self, name="TicketReceiver")

    def receiveMessages(self):
        while True:
            for message in self.queue.receive_messages(WaitTimeSeconds=10):
                print("Ticket:", message.body)
                # TODO print ticket
                message.delete()
    
    def run(self):
        sqs = boto3.resource("sqs")
        self.queue = sqs.get_queue_by_name(QueueName="print-dev-1")
        self.receiveMessages()



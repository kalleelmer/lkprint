import boto3

sqs = boto3.resource("sqs")
queue = sqs.get_queue_by_name(QueueName="print-dev-1")
data = "Some ticket"
queue.send_message(MessageBody=data)

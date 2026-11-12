import json
import boto3
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("EventProcessingResults")


def lambda_handler(event, context):
    for record in event["Records"]:
        message_body = json.loads(record["body"])

        # SNS messages contain the actual event inside "Message".
        if "Message" in message_body:
            event_data = json.loads(message_body["Message"])
        else:
            event_data = message_body

        event_id = str(uuid.uuid4())

        table.put_item(
            Item={
                "event_id": event_id,
                "event_data": event_data,
                "status": "PROCESSED",
                "processed_at": datetime.now(timezone.utc).isoformat()
            }
        )

        print("Event processed successfully:", event_id)

    return {
        "statusCode": 200,
        "body": "Events processed successfully"
    }

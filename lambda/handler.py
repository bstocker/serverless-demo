import json
import boto3
import os

def handler(event, context):
print("EVENT DEBUG:", json.dumps(event))
 
    table_name = os.environ.get("TABLE_NAME")
    if not table_name:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "TABLE_NAME not set"})
        }

    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-east-1',
        endpoint_url='http://ip10-0-6-5-cvhtafqb9qb14bivkpqg-4566.direct.lab-boris.fr',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )
    table = dynamodb.Table(table_name)

    raw_path = event.get("rawPath", "")
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    normalized_path = raw_path.rstrip("/").split("/")[-1].lower()

    if normalized_path == "hello" and method == "GET":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Hello from Lambda!"})
        }

    elif normalized_path == "contact" and method == "POST":
        try:
            body = json.loads(event.get("body", "{}"))
            item = {
                "email": body.get("email"),
                "name": body.get("name"),
                "message": body.get("message")
            }
            table.put_item(Item=item)
            return {
                "statusCode": 200,
                "body": json.dumps({"status": "saved"})
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    else:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "Not found",
                "path": raw_path,
                "method": method
            })
        }

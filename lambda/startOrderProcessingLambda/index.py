import json, os
import boto3
def handler(event, context):
    client = boto3.client('stepfunctions')
    for record in event['Records']:
        message = json.loads(record['body'])
        
        # Get the State Machine ARN from the environment variable
        state_machine_arn = os.environ['STATE_MACHINE_ARN']

        response = client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(message)
        )
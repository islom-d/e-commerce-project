import boto3, json, logging
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def handler(event, context):
    try:
        # Initializing the AWS clients
        sts = boto3.client('sts')
        sns = boto3.client('sns')
        sqs = boto3.client('sqs')

        # Getting the account ID and region dynamically
        account_id = sts.get_caller_identity().get('Account')
        region = boto3.session.Session().region_name

        # Constructing dynamic SQS URL and SNS ARN
        sqs_url = f'https://sqs.{region}.amazonaws.com/{account_id}/OrdersQueue'
        sns_arn = f'arn:aws:sns:{region}:{account_id}:OrderAlertsTopic'

        # Getting the query parameters
        query_params = event.get('queryStringParameters', {})
        event_type = query_params.get('event', None)
        product_id = query_params.get('product_id', None)
        quantity = query_params.get('quantity', None)
        payment_status = query_params.get('payment_status', "failed")

        # Initializing a response dictionary to store outcomes
        response = {}

        # Creating a message with the dynamic data and any other data passed in the query parameters
        message = {
            "product_id": product_id,
            "quantity": quantity,
            "payment_status": payment_status
        }
        
        # Adding additional parameters to the message
        message.update(query_params)

        if event_type == 'order_placement':            
            # Sending message to SQS Queue for successful order placements
            try:
                sqs_response = sqs.send_message(
                    QueueUrl=sqs_url,
                    MessageBody=json.dumps(message)
                )
                response['sqs_response'] = sqs_response
            except Exception as e:
                logging.error(f"Error sending message to SQS: {e}")
                response['sqs_error'] = str(e)

        if event_type in ['payment_failure', 'out_of_stock']:
            # If it's a critical event, publish message to SNS Topic
            try:
                sns_response = sns.publish(
                    TopicArn=sns_arn,
                    Message=json.dumps(message)
                )
                response['sns_response'] = sns_response
            except Exception as e:
                logging.error(f"Error publishing message to SNS: {e}")
                response['sns_error'] = str(e)

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except Exception as e:
        logging.error(f"Error processing order: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
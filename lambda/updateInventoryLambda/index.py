import logging
import boto3, os
from decimal import Decimal
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)  # Set to the desired logging level, ERROR in this case

# Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'InventoryTable') # Default to 'InventoryTable' if TABLE_NAME is not set
table = dynamodb.Table(table_name)

def handler(event, context):
    try:
        # Extract product_id and quantity from event
        product_id = event.get('product_id')
        quantity = event.get('quantity')
        
        # Validate product_id and quantity
        if not product_id or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Valid product_id and quantity are required")
        
        # Fetch the item details from DynamoDB
        try:
            item = table.get_item(
                Key={'ProductID': product_id}
            ).get('Item')
            if not item:
                raise ValueError("Invalid product_id")
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])
        
        # Calculate the total price
        price = item.get('Price', Decimal('0'))  # Assuming 'Price' is a Decimal
        total_price = price * Decimal(quantity)
        
        # Try to update the item in DynamoDB
        try:
            table.update_item(
                Key={
                    'ProductID': product_id,
                },
                UpdateExpression="set Quantity = Quantity - :q",
                ConditionExpression="Quantity >= :q",
                ExpressionAttributeValues={
                    ':q': quantity
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                raise ValueError(f"Not enough quantity available for {product_id}")
            else:
                raise ValueError(e.response['Error']['Message'])
        
        # Construct and return the response
        response = {
            'productName': item.get('Name', ''),
            'quantity': quantity,
            'totalPrice': str(total_price)  # Convert Decimal to string for JSON serialization
        }
        return response
        
    except Exception as e:
        # Log the error message
        logger.error(f"Error occurred: {str(e)}")
        # Raise an exception to be caught by AWS Step Functions
        raise Exception(str(e))
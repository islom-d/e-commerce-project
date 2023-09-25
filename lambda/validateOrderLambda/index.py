import json, os, boto3
from botocore.exceptions import ClientError

def handler(event, context):
    try:
        # Initialize DynamoDB resource
        dynamodb = boto3.resource('dynamodb')
        table_name = os.environ.get('TABLE_NAME', 'InventoryTable') # Default to 'InventoryTable' if TABLE_NAME is not set
        table = dynamodb.Table(table_name)

        # Get ProductID from the event
        product_id = event.get('product_id')
        if not product_id:
            raise ValueError("Missing ProductID in the event")
        
        try:
            # Get the product item from DynamoDB using ProductID
            response = table.get_item(Key={'ProductID': product_id})
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise ValueError("Error fetching product from DynamoDB")
        
        item = response.get('Item')
        if not item:
            raise ValueError("Invalid ProductID")
        
        # Check if order_quantity is a positive integer
        quantity_str = event.get('quantity')
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Invalid Quantity: must be a positive integer")
        
        # Check the quantity of the product
        available_quantity = item.get('Quantity')
        if available_quantity < quantity:
            raise ValueError(f"Product is out of stock.")
        
        # Update Quantity in the event to ensure it's an integer
        event['quantity'] = quantity
        return event
    except Exception as e:
        raise ValueError(f"OrderValidationError: {str(e)}")
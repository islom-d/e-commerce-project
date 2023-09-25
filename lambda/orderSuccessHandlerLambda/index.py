import json

def handler(event, context):
    detail = event.get('detail', {})
    product_name = detail.get('productName')
    quantity = detail.get('quantity')
    total_price = detail.get('totalPrice')
    
    # Compose the order confirmation message
    message = f"Your order has been confirmed.\nProduct Name: {product_name}\nQuantity: {quantity}\nTotal Price: {total_price}\n"

    # Simulate sending confirmation email by logging the message
    print("Simulated email sent:", message)

    return {
        'statusCode': 200,
        'body': json.dumps('Order confirmation simulated successfully!')
    }
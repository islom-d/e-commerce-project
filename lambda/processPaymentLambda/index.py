def handler(event, context):
    try:
        # Extract payment_status from the event
        payment_status = event.get('payment_status')
        
        if payment_status is None:
            raise ValueError("payment_status is missing in the input event")
        
        # Simulate the payment process
        if payment_status != 'successful':
            raise ValueError("PaymentFailureError: Payment was not successful")
        
        # If payment is successful, add any additional information if needed,
        # and pass the entire event to the next function
        event['message'] = 'Payment processed successfully.'
        return event
    
    except Exception as e:
        # Log the detailed error and raise an exception to move to OrderFailed state.
        raise ValueError(str(e))
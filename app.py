import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    logger.info(f"Received event: {json.dumps(event)}")
    
    response = {
        "statusCode": 200,
        "body": json.dumps("Hello, AWS Lambda!")
    }
    
    logger.info(f"Returning response: {json.dumps(response)}")
    
    return response
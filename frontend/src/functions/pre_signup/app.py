from typing import Dict, Any
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Pre-signup Lambda trigger for Cognito user pool.
    Auto-confirms users and adds custom attributes if needed.
    
    Args:
        event: Cognito pre-signup event
        context: Lambda context
    
    Returns:
        Modified event object
    """
    try:
        user_attributes = event['request']['userAttributes']
        logger.info("Processing pre-signup for user", extra={
            "email": user_attributes.get('email'),
            "user_pool_id": event['userPoolId']
        })

        # Auto-confirm user
        event['response']['autoConfirmUser'] = True
        
        # Auto-verify email
        event['response']['autoVerifyEmail'] = True

        return event

    except Exception as e:
        logger.error("Error in pre-signup handler", exc_info=True)
        raise
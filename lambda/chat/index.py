import os
from typing import Dict, Any

import anthropic
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths

logger = Logger()
tracer = Tracer()
app = APIGatewayRestResolver()

@app.post("/chat")
@tracer.capture_method
def chat() -> Dict[str, Any]:
    """Handle chat request using Claude"""
    try:
        request = app.current_event.json_body
        message = request.get("message")
        
        if not message:
            return {"statusCode": 400, "body": "Message is required"}

        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-3-sonnet-20241022-v2",
            max_tokens=4096,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": message
            }]
        )

        return {
            "statusCode": 200,
            "body": {
                "response": message.content[0].text,
                "finish_reason": message.content[0].stop_reason,
                "usage": {
                    "input_tokens": message.usage.input_tokens,
                    "output_tokens": message.usage.output_tokens
                }
            }
        }

    except Exception as e:
        logger.exception("Error handling chat request")
        return {
            "statusCode": 500,
            "body": str(e)
        }

@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """Lambda handler"""
    return app.resolve(event, context)
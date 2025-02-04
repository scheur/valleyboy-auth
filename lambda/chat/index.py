from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.validation import validate_request_parameters
import boto3
import json
import os
from anthropic import Anthropic

# Initialize Powertools
logger = Logger(service="valleyboy-chat")
tracer = Tracer(service="valleyboy-chat")
metrics = Metrics(namespace="valleyboy", service="chat")
app = APIGatewayRestResolver()

# Initialize clients
bedrock = boto3.client('bedrock-runtime')
anthropic_client = Anthropic()

@app.post("/chat")
@tracer.capture_method
@metrics.log_metrics
def chat():
    try:
        # Extract request body
        request_body = app.current_event.json_body
        messages = request_body.get('messages', [])
        
        # Validate request
        if not messages:
            logger.error("No messages provided in request")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No messages provided"})
            }
        
        # Log request metrics
        metrics.add_metric(name="ChatRequests", unit=MetricUnit.Count, value=1)
        
        # Prepare Claude request
        try:
            response = anthropic_client.messages.create(
                model="claude-3-sonnet-20241022",
                max_tokens=4096,
                messages=messages,
                temperature=0.7
            )
            
            # Log success metrics
            metrics.add_metric(name="SuccessfulChatResponses", unit=MetricUnit.Count, value=1)
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "response": response.content[0].text,
                    "usage": {
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens
                    }
                })
            }
            
        except Exception as e:
            logger.exception("Error calling Claude API")
            metrics.add_metric(name="FailedChatResponses", unit=MetricUnit.Count, value=1)
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Failed to get response from Claude"})
            }
            
    except Exception as e:
        logger.exception("Error processing request")
        metrics.add_metric(name="ErrorRequests", unit=MetricUnit.Count, value=1)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }

@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
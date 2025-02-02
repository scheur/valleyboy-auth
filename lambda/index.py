import json
import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
tracer = Tracer()
bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: dict, context: LambdaContext) -> dict:
    try:
        body = json.loads(event['body'])
        messages = body.get('messages', [])
        
        # Prepare request for Claude
        request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": messages,
            "model": "anthropic.claude-3-sonnet-20241022-v2:0"
        }
        
        response = bedrock.invoke_model(
            body=json.dumps(request),
            modelId="anthropic.claude-3-sonnet-20241022-v2:0",
            contentType="application/json",
            accept="application/json"
        )
        
        response_body = json.loads(response['body'].read())
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': response_body['content'][0]['text']
            })
        }
    except Exception as e:
        logger.exception("Error processing request")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }
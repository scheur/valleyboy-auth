import pytest
from unittest.mock import patch, MagicMock
from index import app

@pytest.fixture
def api_gateway_event():
    return {
        "body": '{"messages": [{"role": "user", "content": "Hello"}]}',
        "requestContext": {
            "http": {
                "method": "POST",
                "path": "/chat"
            }
        }
    }

@pytest.fixture
def lambda_context():
    return MagicMock()

def test_chat_success(api_gateway_event, lambda_context):
    with patch('anthropic.Anthropic') as mock_anthropic:
        # Mock successful response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Hello! How can I help you?")]
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 20
        mock_anthropic.return_value.messages.create.return_value = mock_response

        # Call handler
        response = app.resolve(api_gateway_event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "response" in body
        assert "usage" in body

def test_chat_no_messages(api_gateway_event, lambda_context):
    api_gateway_event["body"] = "{}"
    response = app.resolve(api_gateway_event, lambda_context)
    assert response["statusCode"] == 400

def test_chat_api_error(api_gateway_event, lambda_context):
    with patch('anthropic.Anthropic') as mock_anthropic:
        mock_anthropic.return_value.messages.create.side_effect = Exception("API Error")
        response = app.resolve(api_gateway_event, lambda_context)
        assert response["statusCode"] == 500
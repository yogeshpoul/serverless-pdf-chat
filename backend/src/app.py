from flask import Flask, request, jsonify
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def handle_lambda_request(lambda_handler):
    def wrapper(documentid):
        # Extract user ID from headers
        user_id = request.headers.get('user_id', 'test-user-id')
        
        # Construct the event object
        event = {
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "sub": user_id
                    }
                }
            },
            "pathParameters": {
                "documentid": documentid
            }
        }
        
        # Create a mock Lambda context
        class LambdaContext:
            def __init__(self):
                self.function_name = "test-function"
                self.memory_limit_in_mb = 128
                self.invoked_function_arn = "arn:aws:lambda:us-west-2:123456789012:function:test-function"
                self.aws_request_id = "test-request-id"
        
        context = LambdaContext()
        result = lambda_handler(event, context)
        return jsonify(json.loads(result['body'])), result['statusCode']
    
    return wrapper

# Import handlers from other files
from add_conversation.main import lambda_handler as add_conversation_handler
from delete_document.main import lambda_handler as delete_document_handler
# Import other handlers as needed

# API Routes
@app.route('/add_conversation/<documentid>', methods=['POST'])
def add_conversation(documentid):
    return handle_lambda_request(add_conversation_handler)(documentid)

@app.route('/delete_document/<documentid>', methods=['DELETE'])
def delete_document(documentid):
    return handle_lambda_request(delete_document_handler)(documentid)

# Other routes go here...

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

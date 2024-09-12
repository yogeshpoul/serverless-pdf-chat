from flask import Flask, request, jsonify
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def handle_lambda_request(lambda_handler):
    def wrapper(*path_params):
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
            "pathParameters": {}
        }

        # Dynamically add path parameters based on the request
        if path_params:
            if len(path_params) == 1:
                event["pathParameters"]["documentid"] = path_params[0]
            elif len(path_params) == 2:
                event["pathParameters"]["documentid"] = path_params[0]
                event["pathParameters"]["conversationid"] = path_params[1]

        # Create a mock Lambda context
        class LambdaContext:
            def __init__(self):
                self.function_name = "test-function"
                self.memory_limit_in_mb = 128
                self.invoked_function_arn = "arn:aws:lambda:us-west-2:123456789012:function:test-function"
                self.aws_request_id = "test-request-id"

        context = LambdaContext()

        try:
            result = lambda_handler(event, context)
            return jsonify(json.loads(result['body'])), result['statusCode']
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return wrapper

# Import handlers from other files
from add_conversation.main import lambda_handler as add_conversation_handler
from delete_document.main import lambda_handler as delete_document_handler
from generate_embeddings.main import lambda_handler as generate_embeddings_handler
from get_all_documents.main import lambda_handler as get_all_documents_handler
from get_document.main import lambda_handler as get_document_handler
from upload_trigger.main import lambda_handler as upload_trigger_handler
from generate_presigned_url.main import lambda_handler as generate_presigned_url_handler
from generate_response.main import lambda_handler as generate_response_handler

# API Routes
@app.route('/add_conversation/<documentid>', methods=['POST'])
def add_conversation(documentid):
    return handle_lambda_request(add_conversation_handler)(documentid)

@app.route('/delete_document/<documentid>', methods=['DELETE'])
def delete_document(documentid):
    return handle_lambda_request(delete_document_handler)(documentid)

@app.route('/generate_embeddings/<documentid>/<conversationid>', methods=['POST'])
def generate_embeddings(documentid, conversationid):
    return handle_lambda_request(generate_embeddings_handler)(documentid, conversationid)

# API route for generating pre-signed URL
@app.route('/generate_presigned_url', methods=['GET'])
def generate_presigned_url():
    return handle_lambda_request(generate_presigned_url_handler)()

# API route for generating response
@app.route('/<documentid>/<conversationid>', methods=['POST'])
def generate_response(documentid, conversationid):
    return handle_lambda_request(generate_response_handler)(documentid, conversationid)

# API route for getting all documents
@app.route('/doc', methods=['GET'])
def get_all_documents():
    return handle_lambda_request(get_all_documents_handler)()

# API route for getting a specific document
@app.route('/doc/<documentid>/<conversationid>', methods=['GET'])
def get_document(documentid, conversationid):
    return handle_lambda_request(get_document_handler)(documentid, conversationid)

# API route for upload trigger
@app.route('/upload_trigger', methods=['POST'])
def upload_trigger():
    return handle_lambda_request(upload_trigger_handler)()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

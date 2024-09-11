if __name__ == "__main__":
    event = {
        "requestContext": {"authorizer": {"claims": {"sub": "test-user-id"}}},
        "pathParameters": {"documentid": "test-doc-id"}
    }
    context = {}  # You can mock context as necessary
    result = lambda_handler(event, context)
    print(result)

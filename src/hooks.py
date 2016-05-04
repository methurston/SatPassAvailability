"""Module to centralize hooks for @before and @after handlers."""
import json

def validate_type_json(req, resp, resource, params):
    """This function verifys that request is sent as application/json and that the JSON is valid"""
    if req.content_type != 'application/json':
        msg = 'Content must be sent as application/json'
        raise falcon.HTTPUnsupportedMediaType(msg)
    api_input = req.stream.read().decode()
    try:
        input_object = json.loads(api_input)
        params['input_object'] = input_object
    except ValueError as error_details:
        raise falcon.HTTPBadRequest(error_details.args[0])
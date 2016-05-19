"""Module to centralize hooks for @before and @after handlers."""
import json
import falcon


def validate_type_json(req, resp, resource, params):
    """This function verifys that request is sent as application/json and that the JSON is valid
        Returns an input_object parameter to the calling function"""
    if req.content_type != 'application/json':
        msg = 'Content must be sent as application/json'
        raise falcon.HTTPUnsupportedMediaType(msg)
    api_input = req.stream.read().decode()
    print(api_input)
    try:
        input_object = json.loads(api_input)
        params['input_object'] = input_object
    except ValueError as error_details:
        msg = 'Invalid JSON'
        raise falcon.HTTPBadRequest(msg, error_details.args[0])


def get_sat_names(req, resp, resource, params):
    """Unpacks the satellite value provided in params.
    Sets sat_list param to a list of string names for sats."""
    try:
        sat_name = req.params['satellite']
        if isinstance(sat_name, str):
            if sat_name.find(',') != -1:
                req.params['sat_list'] = sat_name.upper().split(',')
            else:
                req.params['sat_list'] = [sat_name.upper()]
        elif isinstance(sat_name, list):
            req.params['sat_list'] = [sat.upper() for sat in sat_name]
        else:
            msg = 'invalid type passed for satellite'
            raise falcon.HTTPBadRequest(msg, sat_name)
    except KeyError as k:
        msg = 'Missing parameter'
        raise falcon.HTTPBadRequest(msg, k.args[0])

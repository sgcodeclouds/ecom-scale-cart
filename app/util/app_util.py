# utils.py

from flask import jsonify

def generate_response(success, message, data=None, errors=None):
    """
    Generates a standardized response structure for Flask API.
    
    :param success: bool indicating the success status of the response
    :param message: str providing a message for the response
    :param data: dict (optional) containing the data for the response
    :param errors: dict (optional) containing the errors for the response
    :return: Flask response object (json)
    """
    response = {
        "success": success,
        "message": message
    }
    
    if data is not None:
        response["data"] = data
    
    if errors is not None:
        response["errors"] = errors

    return jsonify(response)

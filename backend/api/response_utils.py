"""
Utilities for standardized API responses.
All API endpoints should use these functions for consistent response formatting.
"""

from rest_framework.response import Response
from rest_framework import status


def success_response(message=None, data=None, status_code=status.HTTP_200_OK):
    """
    Return a standardized success response.

    Args:
        message: Optional success message
        data: Optional data payload
        status_code: HTTP status code (default: 200)

    Returns:
        Response object with standardized success format
    """
    response_data = {
        'success': True,
    }

    if message:
        response_data['message'] = message

    if data is not None:
        response_data['data'] = data

    return Response(response_data, status=status_code)


def error_response(message, details=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Return a standardized error response.

    Args:
        message: Error message (user-friendly)
        details: Optional detailed error information
        status_code: HTTP status code (default: 400)

    Returns:
        Response object with standardized error format
    """
    response_data = {
        'success': False,
        'error': message,
    }

    if details:
        response_data['details'] = details

    return Response(response_data, status=status_code)


def validation_error_response(errors, message="Validation failed"):
    """
    Return a standardized validation error response.

    Args:
        errors: Validation errors (dict or list)
        message: Optional custom message

    Returns:
        Response object with standardized validation error format
    """
    return Response(
        {
            'success': False,
            'error': message,
            'validation_errors': errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


def not_found_response(message="Resource not found"):
    """
    Return a standardized 404 not found response.

    Args:
        message: Not found message

    Returns:
        Response object with 404 status
    """
    return Response(
        {
            'success': False,
            'error': message
        },
        status=status.HTTP_404_NOT_FOUND
    )


def conflict_response(message, details=None):
    """
    Return a standardized 409 conflict response.

    Args:
        message: Conflict message
        details: Optional detailed conflict information

    Returns:
        Response object with 409 status
    """
    return error_response(
        message=message,
        details=details,
        status_code=status.HTTP_409_CONFLICT
    )


def server_error_response(message="An internal server error occurred", details=None):
    """
    Return a standardized 500 server error response.

    Args:
        message: Error message
        details: Optional detailed error information (include only in development)

    Returns:
        Response object with 500 status
    """
    return error_response(
        message=message,
        details=details,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

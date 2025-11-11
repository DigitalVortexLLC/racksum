"""
Custom exception handlers for Django REST Framework.
Ensures all API errors return consistent response format.
"""

from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from django.db import IntegrityError
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns standardized error responses.

    Args:
        exc: The exception raised
        context: Context information about the request

    Returns:
        Response object with standardized error format
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    # If DRF handled it, format the response
    if response is not None:
        error_data = {
            'success': False,
            'error': None,
        }

        # Handle ValidationError
        if isinstance(exc, ValidationError):
            error_data['error'] = "Validation failed"
            error_data['validation_errors'] = response.data
        # Handle other DRF exceptions
        else:
            # Try to extract error message
            if isinstance(response.data, dict):
                if 'detail' in response.data:
                    error_data['error'] = response.data['detail']
                else:
                    error_data['error'] = str(response.data)
            else:
                error_data['error'] = str(response.data)

        response.data = error_data
        return response

    # Handle exceptions not handled by DRF

    # Handle Django ValidationError
    if isinstance(exc, DjangoValidationError):
        error_data = {
            'success': False,
            'error': "Validation failed",
        }

        if hasattr(exc, 'message_dict'):
            error_data['validation_errors'] = exc.message_dict
        elif hasattr(exc, 'messages'):
            error_data['error'] = ', '.join(exc.messages)
        else:
            error_data['error'] = str(exc)

        from rest_framework.response import Response
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    # Handle Http404
    if isinstance(exc, Http404):
        error_data = {
            'success': False,
            'error': "Resource not found",
        }
        from rest_framework.response import Response
        return Response(error_data, status=status.HTTP_404_NOT_FOUND)

    # Handle IntegrityError (database constraint violations)
    if isinstance(exc, IntegrityError):
        error_data = {
            'success': False,
            'error': "A database constraint was violated",
            'details': str(exc)
        }
        from rest_framework.response import Response
        return Response(error_data, status=status.HTTP_409_CONFLICT)

    # For all other exceptions, return None to let Django handle it
    return None

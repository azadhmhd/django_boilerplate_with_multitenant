# Custom Exception Handling Functions
# These functions handle various exceptions and return a formatted list of errors.

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback
from rest_framework.exceptions import APIException


def handle_404(exc):
    """
        Handle 404 errors (Not Found) and return a standardized error response.
    """
    errors = [
        {
            'field': 'non_field_error',
            'code': 'not_found',
            'message': 'Request not found'
        }
    ]
    return errors


def handle_4xx(exc):
    """
        Handle 4xx errors (Client errors) and return a standardized error response.
    """
    errors = []
    codes = exc.get_codes()
    if isinstance(codes, dict):
        for key in codes:
            errors.append(
                {
                    'field': key,
                    'code': codes[key][0],
                    'message': exc.detail[key][0]
                }
            )
    elif isinstance(codes, str):
        errors.append(
            {
                'field': 'non_field_error',
                'code': exc.get_codes(),
                'message': exc.detail
            }
        )
    elif isinstance(codes, list):
        for ind, value in enumerate(codes):
            if isinstance(value, str):
                errors.append(
                    {
                        'field': 'non_field_error',
                        'code': value,
                        'message': exc.detail[ind]
                    }
                )
            else:
                for index, key in enumerate(value):
                    errors.append(
                        {
                            'field': key,
                            'code': value[key][index],
                            'message': exc.detail[index][key][0]
                        }
                    )
    return errors


def handle_400(exc):
    """
        Handle 400 errors (Bad Request) and return a standardized error response.
    """
    errors = []
    codes = exc.get_codes()
    if isinstance(codes, dict):
        for key in codes:
            errors.append(
                {
                    'field': key,
                    'code': codes[key][0],
                    'message': exc.detail[key][0]
                }
            )
    elif isinstance(exc.get_codes(), str):
        errors.append(
            {
                'field': 'non_field_error',
                'code': exc.get_codes(),
                'message': exc.detail
            }
        )
    else:
        for cc in codes:
            for index, key in enumerate(cc):
                errors.append(
                    {
                        'field': key,
                        'code': cc[key][index],
                        'message': exc.detail[index][key][0]
                    }
                )
    return errors


def handle_401(exc):
    """
        Handle 401 errors (Unauthorized) and return a standardized error response.
    """
    errors = []
    if isinstance(exc.get_codes(), dict):
        errors.append(
            {
                'field': 'token',
                'code': exc.get_codes()['code'],
                'message': exc.detail['detail']
            }
        )
    elif isinstance(exc.get_codes(), str):
        errors.append(
            {
                'field': 'token',
                'code': exc.get_codes(),
                'message': exc.detail
            }
        )
    else:
        errors.append(
            {
                'field': 'token',
                'code': exc.get_codes(),
                'message': exc.detail
            }
        )
    return errors


def more_exception_handler(exc, context):
    """
        Custom exception handler that handles IntegrityError and ValidationError.
        Returns a standardized error response.
    """
    def err_response(exception):
        set_rollback()
        return Response(exception, status=status.HTTP_400_BAD_REQUEST, headers={})
    if isinstance(exc, IntegrityError):
        if isinstance(exc, ProtectedError):
            exc = APIException(detail='Unable to delete, Given object is referenced to other object', code='deletion_protected')
        else:
            exc = APIException(detail='Given value already exist', code='unique')
        return err_response(exc)
    elif isinstance(exc, ValidationError):
        exc = APIException(detail=exc.messages, code='invalid')
        return err_response(exc)
    return None


def custom_exception_handler(exc, context):
    """
        Custom exception handler that calls the appropriate error handling functions
        based on the type of exception and returns a standardized error response.
    """
    response = exception_handler(exc, context)
    if response is None:
        response = more_exception_handler(exc, context)
        if response:
            exc = response.data
    if response is not None:
        try:
            response.data = {'status': response.status_code}
            if response.status_code in [400, 404]:
                response.data['details'] = handle_4xx(exc)
            elif response.status_code in [401, 403]:
                #TODO need to handle this also in 4xx method
                response.data['details'] = handle_401(exc)
        except:
            response = exception_handler(exc, context)
            response['status'] = response.status_code
            return response
    return response


# Custom API Exception Classes

class NoDataForReport(APIException):
    """
        Custom APIException for when there is no data available for a requested input.
    """
    status_code = 400
    default_detail = "No data for requested input"
    default_code = "no_data"


class UserAlreadyExists(APIException):
    """
        Custom APIException for when a user already exists.
    """
    status_code = 400
    default_detail = "User already exists"
    default_code = "unique"


class UserInviteTokenNotExists(APIException):
    """
        Custom APIException for when an invite token does not exist.
    """
    status_code = 404
    default_detail = "Invite token not exists"
    default_code = "not_found"

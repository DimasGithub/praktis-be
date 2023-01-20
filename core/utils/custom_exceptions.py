from rest_framework.exceptions import APIException
from rest_framework import status
class CustomException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'An error occurred on the server.'
    default_code = 'custom_exception'
from rest_framework import status
from rest_framework.response import Response
class ApiResponse:
    def __init__(self, status:int = status.HTTP_500_INTERNAL_SERVER_ERROR, message:str= 'An error occurred on the server.', data=[]):
        self.status = status
        self.message = message
        self.data = data

    def to_response(self):
        return Response(data={'status': self.status, 'message': self.message, 'data': self.data}, status=self.status)
    
    def set_success(self,message, data=[]):
        self.status = status.HTTP_200_OK
        self.message = message
        self.data = data
        return self.to_response()
    
    def set_created_success(self, message, data=[]):
        self.status = status.HTTP_201_CREATED
        self.message = message
        self.data = data
        return self.to_response()
    
    def set_bad_request(self, message):
        self.status = status.HTTP_400_BAD_REQUEST
        self.message = message
        return self.to_response()
    
    def set_not_found(self, message):
        self.status = status.HTTP_404_NOT_FOUND
        self.message = message
        return self.to_response()
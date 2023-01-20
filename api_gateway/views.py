import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
class ApiGatewayUser(APIView):
    def __init__(self) -> None:
        self.context_header = {'Authorization': "Token "+f"{settings.SERVICE_TOKEN_RPC}"}
        self.url = f'{settings.BASE_SERVICE_URL}/user/'

    def request_base(self, method, data= None):
        response = requests.request(method, url=f"{self.url}", data=data, headers=self.context_header)
        return Response(response.json())

    def post(self, request):
        data = {
            'name': str(request.data['name']).lower(),
            'type': str(request.data['type']).upper()
        }
        return self.request_base('post', data=data)

    def get(self,request):
        return self.request_base('get')

class ApiGatewayUserDetail(APIView):
    def __init__(self) -> None:
        self.context_header = {'Authorization': "Token "+f"{settings.SERVICE_TOKEN_RPC}"}
        self.url = f'{settings.BASE_SERVICE_URL}/user'
    
    def request_base(self, method, uuid, data= None):
        response = requests.request(method, url=f"{self.url}/{uuid}", data=data, headers=self.context_header)
        return Response(response.json())
        
    def put(self, request, uuid):
        data = {
            'name': request.data['name'],
            'type': request.data['type']
        } 
        return self.request_base('put',uuid=uuid, data=data)

    def get(self, request, uuid):
        return self.request_base('get',uuid=uuid)

    def delete(self,request, uuid):
        return self.request_base('delete', uuid=uuid)

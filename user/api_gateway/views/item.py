import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
class ApiGatewayItem(APIView):
    def __init__(self) -> None:
        self.context_header = {'Content-Type': 'application/json; charset=UTF-8','Authorization': "Token "+f"{settings.SERVICE_TOKEN_RPC}"}
        self.url = f'{settings.BASE_SERVICE_URL}/item/'
    def request_base(self, method, data= None):
        response = requests.request(method, url=f"{self.url}", data=data, headers=self.context_header)
        return Response(response.json())
    def post(self, request):
        data = {
            'name':request.data['name'],
            'type':request.data['type'],
            'prices':request.data['prices']
        }
        return self.request_base('post', data=json.dumps(data))

    def get(self,request):
        return self.request_base('get')

class ApiGatewayItemDetail(APIView):
    def __init__(self) -> None:
        self.context_header = {'Content-Type': 'application/json; charset=UTF-8','Authorization': "Token "+f"{settings.SERVICE_TOKEN_RPC}"}
        self.url = f'{settings.BASE_SERVICE_URL}/item'
    
    def request_base(self, method, uuid, data= None):
        response = requests.request(method, url=f"{self.url}/{uuid}", data=json.dumps(data), headers=self.context_header)
        return Response(response.json())
    
    def get(self,request, uuid):
        return self.request_base('get', uuid=uuid)

    def put(self, request, uuid):
        data = {
            'name':request.data['name'],
            'type':request.data['type'],
            'prices':request.data['prices']
        } 
        return self.request_base('put',uuid=uuid, data=data)
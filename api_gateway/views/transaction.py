import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

class ApiGatewayTransaction(APIView):
    def __init__(self) -> None:
        self.context_header = {'Content-Type': 'application/json; charset=UTF-8','Authorization': "Token "+f"{settings.SERVICE_TOKEN_RPC}"}
        self.url = f'{settings.BASE_SERVICE_URL}/transaction/'
    def request_base(self, method, data= None):
        response = requests.request(method, url=f"{self.url}", data=data, headers=self.context_header)
        return Response(response.json())
    def post(self, request):
        data = {
            'transaction':request.data['transaction']
        }
        return self.request_base('post', data=json.dumps(data))
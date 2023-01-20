from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework import status

class ApigatewayTokenAuth(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed({'status':status.HTTP_401_UNAUTHORIZED,'message':'Invalid Token!.', 'data':[]})

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed({'status':status.HTTP_401_UNAUTHORIZED,'message':'User unactivated!.', 'data':[]})

        return (token.user, token)
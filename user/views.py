from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from core.utils.custom_permission import ServicePermissionAccess
from core.utils.custom_authtoken import ApigatewayTokenAuth
from core.utils.custom_response import ApiResponse

from user.models import User, UserType
from user.serializer import UserSerializer

class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    authentication_classes = (ApigatewayTokenAuth,)
    permission_classes = (ServicePermissionAccess,)

    def post(self, request):
        try:
            response = ApiResponse()
            data = {
                'name': str(request.data['name']).lower(),
                'type': str(request.data['type']).upper()
            }
            if not data.get('type') in dict(UserType.choices): return response.set_bad_request(message="Input User Type Invalid!.")
            users = User.objects.filter(name__iexact=data.get('name'))
            if users: return response.set_bad_request(message="Name item already exists.")
            else:
                serializer = UserSerializer(data = data)
                if serializer.is_valid():
                    serializer.save()
                    response = response.set_created_success(message="User name create is success.", data=serializer.data)
                else:
                    response = response.set_bad_request(message=str(serializer.errors))
        except Exception as err:
            response = response.set_bad_request(message=str(err))
        return response
    
    def list(self,request):
        try:
            response = ApiResponse()
            users = User.objects.filter(deleted_at__isnull=True)
            if users:
                serializer = self.get_serializer(users, many=True)
                response = response.set_success(message="Data user is found.", data=serializer.data)
            else:
                response = response.set_not_found(message="Data user not found!.")
        except Exception as err:
            response = response.set_bad_request(message=err)
        return response
    
    def delete(self,request, uuid):
        try:
            response = ApiResponse()
            user = User.objects.get(uuid=uuid)
            user.delete()
            response = response.set_success(message="User deleted successful.")

        except User.DoesNotExist:
            response = response.set_not_found(message="User not found!.")
        except Exception as err:
            response = response.set_bad_request(message=str(err))
        return response

    def put(self, request, uuid):
        try:
            response = ApiResponse()
            data = {
                'name': str(request.data['name']).lower(),
                'type': str(request.data['type']).upper()
            }
            if not data.get('type') in dict(UserType.choices): raise ValidationError({'status':status.HTTP_400_BAD_REQUEST, 'message': 'User type invalid!.', 'data':[]})
            user = User.objects.get(uuid=uuid)
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                response = response.set_success(message="User updated is success.", data=serializer.data)
            else:
                response = response.set_bad_request(message=str(serializer.errors))
        except User.DoesNotExist:
            response = response.set_not_found(message="Data user not found!.")
        except Exception as err:
            response = response.set_bad_request(message=str(err))
        return response

    def get(self,request, uuid):
        try:
            response = ApiResponse()
            user = User.objects.get(uuid=uuid)
            serializer = self.get_serializer(user)
            response = response.set_success(message="Data user is found.", data=serializer.data)
        except User.DoesNotExist:
            response = response.set_not_found(message="Data user not found!.")
        
        except Exception as err:
            response = response.set_bad_request(message=str(err))
            
        return response
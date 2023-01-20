from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError

from item.serializer import ItemSerializer
from item.models import ItemType, Item, ItemPrice
from user.models import UserType

from core.utils.custom_permission import ServicePermissionAccess
from core.utils.custom_authtoken import ApigatewayTokenAuth
from core.utils.custom_response import ApiResponse


class ItemViewSet(viewsets.GenericViewSet):
    serializer_class = ItemSerializer
    authentication_classes = (ApigatewayTokenAuth,)
    permission_classes = (ServicePermissionAccess,)

    def post(self, request):
        response = ApiResponse()
        try:
            data = {
                'name': str(request.data['name']).lower(),
                'type': str(request.data['type']).lower(),
                'prices': request.data['prices'],
            }
            #validate type
            if not data.get('type') in dict(ItemType.choices): return response.set_bad_request(message="Input Item Type Invalid!.")
            
            have_regular_price = False
            #validate prices
            for price in data.get('prices'):
                #check regular prices
                if str(price.get('pricefor')).upper() == UserType.REGULAR: have_regular_price = True
                if not str(price.get('pricefor')).upper() in dict(UserType.choices): return response.set_bad_request(message="Input priceFor Invalid!.") 
                if price.get('price')<= 0: return response.set_bad_request(message="Input price invalid!.")

            #check item have regular price 
            if not have_regular_price: return response.set_bad_request(message="Item must have a regular price!.")
            
            #check unique name item
            items = Item.objects.filter(name__iexact=data.get('name'))
            if items: return response.set_bad_request(message="Name item already exists!.")

            item = Item.objects.create(name = data.get('name'), type=data.get('type'))
            item.save()
            for price in data.get('prices'):
                itemprice, created= ItemPrice.objects.get_or_create(item = item, pricefor=price.get('pricefor'))
                if created:
                    itemprice.price = price.get('price')
                    itemprice.save()
            serializer = ItemSerializer(item)
            response = response.set_created_success(message="Data item create is success.", data=serializer.data)
        except Exception as err:
            response = response.set_bad_request(message=str(err))
        return response

    def list(self, request):
        try:
            response = ApiResponse()
            items = Item.objects.filter(deleted_at__isnull=True)
            if items:
                serializer = self.get_serializer(items, many=True)
                response = response.set_success(message="Data item is found.", data=serializer.data)
            else:
                response = response.set_not_found(message="Data item not found!.")
        
        except Exception as err:
            response = response.set_bad_request(message=str(err))

        return response

    def delete(self, request, uuid):
        try:
            response = ApiResponse()
            user = Item.objects.get(uuid=uuid)
            user.delete()
            response = response.set_success(message="Item deleted is successful.")

        except Item.DoesNotExist:
            response = response.set_not_found(message="Data item not found!.")

        except Exception as err:
            response = response.set_bad_request(message=str(err))

        return response

    def put(self, request, uuid):
        try:
            response = ApiResponse()
            item = Item.objects.get(uuid=uuid)
            data = {
                'name': str(request.data['name']).lower(),
                'type': str(request.data['type']).lower(),
                'prices': request.data['prices']
            }

            #validate type
            if not data.get('type') in dict(ItemType.choices): return response.set_bad_request(message="Input Item Type Invalid!.")
            
            have_regular_price = False
            #validate prices
            for price in data.get('prices'):
                if str(price.get('pricefor')).upper() == UserType.REGULAR: have_regular_price = True
                if not str(price.get('pricefor')).upper() in dict(UserType.choices): return response.set_bad_request(message="Input priceFor Invalid!.") 
                if price.get('price')<= 0: return response.set_bad_request(message="Input price invalid!.")
            
            #check item have regular price            
            if not have_regular_price: return response.set_bad_request(message="Item must have a regular price!.")

            #validate name item unique
            items = Item.objects.filter(name__iexact=data.get('name')).exclude(name__iexact=item.name)
            if items: return response.set_bad_request(message="Name item already exists!.")
            else:
                item.name = data.get('name')
                item.type = data.get('type')
                item.save()
                for price in data.get('prices'):
                    pricefor = str(price.get('pricefor')).upper()
                    item_price, created = ItemPrice.objects.get_or_create(item = item, pricefor=pricefor)
                    if created:
                        item_price.price = price.get('price')
                        item_price.save()
                    else:
                        item_price.price = price.get('price')
                        item_price.save()
                serializer = self.get_serializer(item)
                response = response.set_success(message="Data item is updated.", data=serializer.data)
        except Item.DoesNotExist:
            response = response.set_not_found(message="Data item not found!.")
        
        except Exception as err:
            response = response.set_bad_request(message=str(err))
        
        return response

    def get(self, request, uuid):
        try:
            response = ApiResponse()
            item = Item.objects.get(uuid=uuid)
            serializer = self.get_serializer(item)
            response = response.set_success(message="Data item is found.", data=serializer.data)
        except Item.DoesNotExist:
            response = response.set_not_found(message="Data item not found!.")

        except Exception as err:
            response = response.set_bad_request(message=str(err))

        return response

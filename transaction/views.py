from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from core.utils.custom_permission import ServicePermissionAccess
from core.utils.custom_authtoken import ApigatewayTokenAuth
from core.utils.custom_response import ApiResponse

from user.models import User, UserType
from transaction.models import Transaction
from transaction.serializer import TransactionSerializer
from item.models import Item
from user.models import User

class TransactionViewSet(viewsets.GenericViewSet):
    serializer_class = TransactionSerializer
    authentication_classes = (ApigatewayTokenAuth,)
    permission_classes = (ServicePermissionAccess,)

    def is_duplicate_transactions(self,transactions):
        if len(transactions) > 0:
            x = 0
            while x < len(transactions):
                d = transactions[x]
                y = 0
                while y < len(transactions):
                    z = transactions[y]
                    if x != y and (d.get('item') == z.get('item') and d.get('buyer') == z.get('buyer')):
                        return True
                    y+=1
                x+=1
        return False

    def is_valid_buyer_or_item(self,transactions):
        try:
            x = 0
            while x < len(transactions):
                buyer = transactions[x].get('buyer') 
                item = transactions[x].get('item')
                User.objects.get(name__iexact=buyer)
                Item.objects.get(name__iexact=item)
                x+=1
            return True
        except (User.DoesNotExist, Item.DoesNotExist):
            return False

    def post(self, request):
        response = ApiResponse()
        transactions = request.data.get('transaction')
        #check transaction duplicate buyer and item
        if self.is_duplicate_transactions(transactions): 
            return response.set_bad_request(message="The transactions has duplicated buyer and item!. Please try again.")

        #check `buyer` and `item` validate
        if not self.is_valid_buyer_or_item(transactions):
            return response.set_bad_request(message="The transactions `item` or `buyer` has undifined!. Please try again.")
        
        if len(transactions)>0:
            for transaction in transactions:
                user = User.objects.get(name__iexact=transaction.get('buyer'))
                item = Item.objects.get(name__iexact=transaction.get('item'))
                transaction = Transaction.objects.create(
                    user = user,
                    item = item,
                    qty = transaction.get('qty')
                )
                transaction.save()

            serializer = self.get_serializer(Transaction.objects.filter(deleted_at__isnull=True))
            response = response.set_created_success(message="create transaction is success", data=serializer.data)
        else:
            response = response.set_bad_request(message="Request invalid!. Try again.")
        return response

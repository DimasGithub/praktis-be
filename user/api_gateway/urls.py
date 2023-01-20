from django.urls import path
from api_gateway.views.user import ApiGatewayUser, ApiGatewayUserDetail
from api_gateway.views.item import ApiGatewayItem, ApiGatewayItemDetail
from api_gateway.views.transaction import ApiGatewayTransaction

urlpatterns = [
    path('user/', ApiGatewayUser.as_view()),
    path('user/<str:uuid>', ApiGatewayUserDetail.as_view()),
    path('item/', ApiGatewayItem.as_view()),
    path('item/<str:uuid>', ApiGatewayItemDetail.as_view()),
    path('transaction/', ApiGatewayTransaction.as_view())
]
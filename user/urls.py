from django.urls import path
from user.views import UserViewSet

urlpatterns = [
    path('', UserViewSet.as_view({'get':'list', 'post':'post'})),
    path('<str:uuid>', UserViewSet.as_view({'get':'get',
                                            'post':'post',
                                            'put':'put', 
                                            'delete':'delete'})),
]
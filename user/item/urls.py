from django.urls import path
from item.views import ItemViewSet

urlpatterns = [
    path('', ItemViewSet.as_view({'get':'list','post':'post'})),
    path('<str:uuid>', ItemViewSet.as_view({'get':'get',
                                            'post':'post',
                                            'put':'put', 
                                            'delete':'delete'})),
]
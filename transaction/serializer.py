from rest_framework import serializers
from transaction.models import Transaction
from item.models import ItemType, Item
from user.models import User

from django.db.models.expressions import OuterRef
from django.db.models.functions import Coalesce
from django.db.models import Subquery
from django.db.models import Sum

class RevenueCategorySerializer(serializers.Serializer):
    item__type = serializers.ChoiceField(choices=ItemType.choices)
    revenue = serializers.IntegerField()
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = data.pop("item__type", "")
        data["revenue"] = data.pop("revenue", "")
        return data

class BestSpenderSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    spent = serializers.SerializerMethodField()

    def get_name(self, obj):
        if obj.name:
            return obj.name
        return 0

    def get_type(self, obj):
        if obj.type:
            return obj.type
        return None
    
    def get_spent(self, obj):
        return obj.get_spent
            

class TransactionSerializer(serializers.ModelSerializer):
    totalTransaction = serializers.SerializerMethodField()
    bestSellingCategory = serializers.SerializerMethodField()
    bestSellingItem = serializers.SerializerMethodField()
    rpc = serializers.SerializerMethodField()
    revenue = serializers.SerializerMethodField()
    bestSpenders = serializers.SerializerMethodField()        
    
    def get_totalTransaction(self, obj):
        return obj.count()
    
    def get_bestSpenders(self, obj):
        user = User.objects.annotate(spent=Sum('users__total_price')).order_by('-spent')[:3]
        return BestSpenderSerializer(user, many=True).data

    def get_rpc(self, obj):
        item = obj.values('item__type').annotate(revenue=Sum('total_price')).order_by('-revenue')
        return RevenueCategorySerializer(item, many=True).data

    def get_bestSellingItem(self, obj):
        item = obj.prefetch_related('item').values('item__name').annotate(total_price=Sum('total_price')).order_by('-total_price').first()
        if item:return item['item__name']

        return None

    def get_bestSellingCategory(self, obj):
        item = obj.values('item__type').annotate(total_price=Sum('total_price')).order_by('-total_price').first()
        if item: return item['item__type']
        return None

    def get_revenue(self, obj):
        return obj.aggregate(Sum('total_price'))['total_price__sum']
    
    class Meta:
        model = Transaction
        fields = ['totalTransaction','bestSellingItem', 'bestSellingCategory', 'rpc', 'revenue', 'bestSpenders']
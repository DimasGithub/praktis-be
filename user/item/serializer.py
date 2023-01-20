import uuid
from rest_framework import serializers
from item.models import Item, ItemType, ItemPrice
from user.models import UserType

class ItemPriceSerializer(serializers.ModelSerializer):
    pricefor = serializers.ChoiceField(choices=UserType.choices)
    price = serializers.IntegerField()
    class Meta:
        model = ItemPrice
        fields = ['pricefor', 'price']

class ItemSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(default=uuid.uuid4, read_only=True)
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=ItemType.choices)
    prices = serializers.SerializerMethodField()
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    deleted_at = serializers.ReadOnlyField()

    def get_prices(self, obj):
        price = ItemPrice.objects.filter(item=obj)
        return ItemPriceSerializer(price,many=True).data

    # def create(self, validated_data):
    #     if 'prices' in validated_data:
    #         prices_data = validated_data.get('prices', [])
    #     else:
    #         raise ValueError("The prices field is missing in the request data")
    #     item = Item.objects.create(**validated_data)
    #     for price_data in prices_data:
    #         price_serializer = ItemPriceSerializer(data=price_data)
    #         price_serializer.is_valid(raise_exception=True)
    #         price_serializer.save(item=item)
    #     return item

    class Meta:
        model = Item
        fields = ['uuid', 'name', 'type', 'prices', 'created_at', 'updated_at', 'deleted_at']
    
    
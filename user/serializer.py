import uuid
from rest_framework import serializers
from user.models import User, UserType

class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(default=uuid.uuid4, read_only=True)
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=UserType.choices)
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    deleted_at = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = '__all__'
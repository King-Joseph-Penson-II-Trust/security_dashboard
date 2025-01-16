from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, BlocklistItem, IPList, DomainList

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}

class BlocklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlocklistItem
        fields = ['id','entry', 'added_by', 'added_on', 'auto_delete', 'delete_date', 'notes']
        extra_kwargs = {"added_by": {"read_only": True}}

    def validate_entry(self, value):
        if not BlocklistItem.is_valid_entry(value):
            raise serializers.ValidationError(f"{value} is not a valid IP address or domain")
        return value

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data['added_by'] = request.user
        else:
            validated_data['added_by'] = None
        return super().create(validated_data)

class IPListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPList
        fields = ['ip', 'added_on']

class DomainListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainList
        fields = ['domain', 'added_on']
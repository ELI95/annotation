from rest_framework import serializers

from targets.models import Target, TargetType


class TargetSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Target
        fields = [
            'id',
            'user',
            'name',
            'type',
            'type_name',
            'entity',
            'description',
        ]
        read_only_fields = ['user']

    def get_type_name(self, obj):
        return obj.type.name


class TargetTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TargetType
        fields = [
            'id',
            'name',
            'chinese_name',
        ]

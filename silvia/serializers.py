
from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=1000,
        allow_blank=False,
        trim_whitespace=True,
    )

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError("Invalid request.")

        allowed_fields = {"message"}
        unknown_fields = set(data.keys()) - allowed_fields

        if unknown_fields:
            raise serializers.ValidationError("Invalid request.")

        return super().to_internal_value(data)

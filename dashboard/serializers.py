from rest_framework import serializers

class TimeSerializer(serializers.Serializer):
    time = serializers.DateTimeField()
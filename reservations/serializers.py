from rest_framework import serializers


class StatisticsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    num_of_reservations = serializers.IntegerField()
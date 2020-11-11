from rest_framework import serializers

class ExposeSerializer(serializers.Serializer):
    kaufpreis = serializers.FloatField(required=False, allow_null=True)
    area = serializers.FloatField(required=False, allow_null=True)
    baujahr = serializers.IntegerField(required=False, allow_null=True)
    wohnflaeche = serializers.FloatField(required=False, allow_null=True)
    gewerbeflaeche = serializers.FloatField(required=False, allow_null=True)
    wohneinheiten = serializers.IntegerField(required=False, allow_null=True)
    gewerbeeinheiten = serializers.IntegerField(required=False, allow_null=True)
    jnkm = serializers.FloatField(required=False, allow_null=True)
    price_m2 = serializers.FloatField(required=False, allow_null=True)
    multiplier = serializers.FloatField(required=False, allow_null=True)
    _yield = serializers.FloatField(source='yield', required=False, allow_null=True)
    address = serializers.CharField(max_length=200, required=False, allow_null=True)
    date = serializers.DateField(required=False, allow_null=True)
    resource = serializers.CharField(max_length=200, required=False, allow_null=True)

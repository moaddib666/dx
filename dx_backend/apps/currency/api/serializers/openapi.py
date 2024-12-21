from rest_framework import serializers

from apps.currency.models import CurrencyToken, PlayerCurrency


class CurrencyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyToken
        fields = ['id', 'name', 'description', 'icon']
        read_only_fields = ['id']


class PlayerCurrencySerializer(serializers.ModelSerializer):
    currency = CurrencyTokenSerializer()

    class Meta:
        model = PlayerCurrency
        fields = ['id', 'player', 'currency', 'amount']
        read_only_fields = ['id', 'player', 'currency', 'amount']

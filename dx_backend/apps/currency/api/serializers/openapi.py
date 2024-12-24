from rest_framework import serializers

from apps.currency.models import CurrencyToken, CharacterCurrency


class CurrencyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyToken
        fields = ['id', 'name', 'description', 'icon']
        read_only_fields = ['id']


class CharacterCurrencySerializer(serializers.ModelSerializer):
    currency = CurrencyTokenSerializer()

    class Meta:
        model = CharacterCurrency
        fields = ['id', 'character', 'currency', 'amount']
        read_only_fields = ['id', 'character', 'currency', 'amount']

from django.db import transaction
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, mixins, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.bargain.api.serializers.openapi import BargainSerializer, BargainCreateSerializer, OfferedItemSerializer, \
    DetailedBargainSerializer
from apps.bargain.models import Bargain, OfferedItem
from apps.character.models import Character
from apps.core.api.utils.character import GenericGameViewSet
from apps.game.services.bargain.gift_item import default_bargain_svc_factory


class OpenBargainViewSet(viewsets.ReadOnlyModelViewSet, GenericGameViewSet):
    queryset = Bargain.objects.filter(cancelled=False, completed=False)
    serializer_class = BargainSerializer
    permission_classes = [permissions.IsAuthenticated]
    factory = default_bargain_svc_factory

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DetailedBargainSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(side_a=self.get_character(), side_a_accepted=False) | qs.filter(side_b=self.get_character(),
                                                                                         side_b_accepted=False)

    @extend_schema(responses={200: BargainSerializer})
    @action(detail=False, methods=['post'], serializer_class=BargainCreateSerializer)
    @transaction.atomic
    def gift(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        character = self.get_character()
        bargain = self.factory.gift_item_from_character(character, get_object_or_404(Character,
                                                                                     id=serializer.validated_data[
                                                                                         'target_character_id']))
        return Response(BargainSerializer(bargain.model).data)

    @extend_schema(responses={200: BargainSerializer})
    @action(detail=True, methods=['post'], serializer_class=serializers.Serializer)
    @transaction.atomic
    def accept(self, request, *args, **kwargs):
        character = self.get_character()
        bargain = self.get_object()
        self.factory.from_bargain(bargain).accept(character)
        return Response(BargainSerializer(bargain).data)

    @extend_schema(responses={200: BargainSerializer})
    @action(detail=True, methods=['post'], serializer_class=serializers.Serializer)
    @transaction.atomic
    def reject(self, request, *args, **kwargs):
        character = self.get_character()
        bargain = self.get_object()
        self.factory.from_bargain(bargain).cancel()
        return Response(BargainSerializer(bargain).data)


class OpenBargainItemsViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                              GenericGameViewSet):
    """ Nested viewset for adding and removing items from a bargain """
    queryset = OfferedItem.objects.all()
    serializer_class = OfferedItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    factory = default_bargain_svc_factory
    lookup_field = "item_id"

    def get_queryset(self):
        character = self.get_character()
        qs = super().get_queryset()
        # FIXME: ensure that OffetreItem is owned by character and the character is in the bargain, and the bargain is not completed or cancelled
        filtered_qs = qs.filter(
            Q(bargain__side_a=character) | Q(bargain__side_b=character),
            bargain_id=self.kwargs['bargain_pk'],
            bargain__cancelled=False,
            bargain__completed=False,
            item__characteritem__character=character  # Ensure OfferedItem belongs to the character
        ).distinct()
        return filtered_qs.prefetch_related('item')

    def perform_create(self, serializer):
        character = self.get_character()
        bargain = get_object_or_404(Bargain, id=self.kwargs['bargain_pk'])
        world_item = serializer.validated_data['item']
        # Check if character has this item (using filter instead of get to handle multiple items)
        if not character.equipped_items.filter(world_item=world_item).exists():
            raise ValidationError("Character does not have this item")
        try:
            self.factory.from_bargain(bargain).add_item(character, world_item)
        except ValueError as e:
            raise ValidationError(str(e)) from e

    def perform_destroy(self, instance):
        character = self.get_character()
        bargain = get_object_or_404(Bargain, id=self.kwargs['bargain_pk'])
        self.factory.from_bargain(bargain).remove_item(character, instance.item)
        instance.delete()

import logging
import typing
from typing import Optional

from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import ResolvedComponent, ComponentRegistry
from drf_spectacular.utils import _SerializerType, _SchemaType
from pydantic import BaseModel

from apps.core.bus.base import GameEvent
from apps.core.bus.registry import DEFAULT_EVENT_REGISTRY


def export_pydantic_model_to_openapi(model: BaseModel, name: str):
    return ResolvedComponent(
        name=name,
        type=ResolvedComponent.SCHEMA,
        schema=model.model_json_schema(),
    )


# drf_spectacular.openapi.AutoSchema
class CustomSchemaGenerator(AutoSchema):
    logger = logging.getLogger("openapi.schema.CustomSchemaGenerator")


    def game_event_name_constructor(self, event: type[GameEvent]) -> str:
        return event.__name__
    def game_event_data_name_constructor(self, name: str) -> str:
        return name

    def add_custom_components(self, registry: ComponentRegistry = None):
        if not registry:
            return
        for event in DEFAULT_EVENT_REGISTRY.get_all_events():
            # let pydantic generate a JSON schema
            name = self.game_event_name_constructor(event)
            self.logger.debug(f"Generating schema for {name}")
            schema = event.model_json_schema(ref_template="#/components/schemas/{model}")
            component = ResolvedComponent(
                name=name,
                type=ResolvedComponent.SCHEMA,
                schema=schema,
            )
            registry.register_on_missing(component)
            for sub_name, sub_schema in schema.pop("$defs", {}).items():
                sub_name = self.game_event_data_name_constructor(sub_name)
                component = ResolvedComponent(
                    name=sub_name,
                    type=ResolvedComponent.SCHEMA,
                    schema=sub_schema,
                )
                registry.register_on_missing(component)

    def get_operation(
            self,
            path: str,
            path_regex: str,
            path_prefix: str,
            method: str,
            registry: ComponentRegistry
    ) -> Optional[_SchemaType]:
        operation = super().get_operation(path, path_regex, path_prefix, method, registry)
        if self.view.__class__.__name__ == "CentrifugoViewSet" and self.view.action == "publish":
            self.add_custom_components(registry=registry)
        return operation
    def get_request_serializer(self) -> Optional[_SerializerType]:
        serializer = super().get_request_serializer()
        if self.view.__class__.__name__ == "CentrifugoViewSet" and self.view.action == "publish":
            event_types = [t.__annotations__["data"] for t in DEFAULT_EVENT_REGISTRY.consumed] or [dict, ]
            request_serializer_type = typing.Union[*tuple(event_types)]

            class GameEventSerializer(GameEvent):
                data: request_serializer_type

            return GameEventSerializer
        return serializer

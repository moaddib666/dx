import dataclasses
import typing

from django.db.models import Model


@dataclasses.dataclass(frozen=True)
class Dependency:
    source: Model
    target: Model
    field: typing
    reverse: bool = False
    layer: int = 0

    def __str__(self):
        return f"Dependency(source={self.source}, target={self.target}, field={self.field}, reverse={self.reverse}, layer={self.layer})"

    def clone(self, source: Model, target: Model) -> 'Dependency':
        """
        Create a clone of the current dependency with a new source and target.
        """
        return Dependency(
            source=source,
            target=target,
            field=self.field,
            reverse=self.reverse,
            layer=self.layer
        )


class DependencyFactory:
    @staticmethod
    def create(source: Model, target: Model, field: typing, reverse: bool = False, layer: int = 0) -> Dependency:
        """
        Factory method to create a Dependency instance.
        """
        return Dependency(
            source=source,
            target=target,
            field=field,
            reverse=reverse,
            layer=layer
        )

    @classmethod
    def create_directed_dependency(cls, source: Model, target: Model, field: typing, layer: int = 0) -> Dependency:
        """
        Create a directed dependency (source -> target).
        """
        return cls.create(source, target, field, reverse=False, layer=layer)

    @classmethod
    def create_reverse_dependency(cls, source: Model, target: Model, field: typing, layer: int = 0) -> Dependency:
        """
        Create a reverse dependency (target -> source).
        """
        return cls.create(source, target, field, reverse=True, layer=layer)

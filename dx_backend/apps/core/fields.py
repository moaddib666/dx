from django.db import models
from django.core.exceptions import ValidationError
import json
from typing import Any, List, Type


class TypedJSONField(models.JSONField):
    """
    A custom JSONField that enforces a specific type structure for its data.
    """

    def __init__(self, *args, required_type: Type[Any] = None, many: bool = False, **kwargs):
        if required_type is None:
            required_type = dict
        self.required_type = required_type
        self.many = many
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        """
        Convert JSON data from the database into the required type.
        """
        value = super().from_db_value(value, expression, connection)
        if value is None:
            return None
        if self.many:
            return [self._deserialize_item(item) for item in value]
        return self._deserialize_item(value)

    def to_python(self, value):
        """
        Convert input value into the required type.
        """
        if isinstance(value, str):
            value = json.loads(value)
        if self.many:
            if not isinstance(value, list):
                raise ValidationError("Expected a list of items.")
            return [self._deserialize_item(item) for item in value]
        return self._deserialize_item(value)

    def get_prep_value(self, value):
        """
        Serialize the required type into JSON for the database.
        """
        if self.many:
            if not isinstance(value, list):
                raise ValidationError(f"Expected a list of {self.required_type.__name__} instances.")
            return [self._serialize_item(item) for item in value]
        return self._serialize_item(value)

    def deconstruct(self):
        """
        Deconstruct the field for migrations as a plain JSONField.
        """
        name, path, args, kwargs = super().deconstruct()
        path = "django.db.models.JSONField"  # Replace TypedJSONField with JSONField in migrations
        return name, path, args, kwargs

    def _deserialize_item(self, item):
        """
        Deserialize an item into the required type.
        """
        if not isinstance(item, dict):
            raise ValidationError(f"Expected a dictionary to deserialize, got {type(item).__name__}.")
        return self.required_type(**item)

    def _serialize_item(self, item):
        """
        Serialize an item into a JSON-compatible dictionary.
        """
        try:
            return self.required_type(**item)
        except Exception as err:
            raise ValidationError(f"Expected an instance of {self.required_type.__name__}, got {type(item).__name__}.") from err

import io

from django.core.serializers.base import Serializer as PythonSerializer


class ModelPresenter:
    def __init__(self, model, stream):
        self.model = model
        self.stream = stream

    def describe_model(self):
        fields = [f"{field.name} ({field.get_internal_type()}): {field.verbose_name or field.name}"
                  for field in self.model._meta.fields]
        self.stream.write(f"Model: {self.model.__name__}\nFields: {', '.join(fields)}\n")

    def describe_instance(self, instance):
        field_values = [f"{field.name}: {getattr(instance, field.name)}"
                        for field in self.model._meta.fields]
        self.stream.write(f"Instance: {self.model.__name__}\nValues: {', '.join(field_values)}\n")


class PathPresenter(ModelPresenter):
    def describe_model(self):
        """
        Provide a description of the Path model.
        """
        self.stream.write(
            f"Model: {self.model.__name__}. Represents unique paths in the game that characters follow, "
            "defining their progression, abilities, and lore.\n"
        )

    def describe_instance(self, instance):
        """
        Provide a single-line detailed description of a path.
        """
        # General path details
        path_id = getattr(instance, "id", "unknown")
        name = getattr(instance, "name", "Unnamed Path")
        description = getattr(instance, "description", "No description provided.")
        # Build single-line description
        line = (
            f"Path ID: {path_id} -> {name} - {description}"
        )
        self.stream.write(line + "\n")


class SchoolPresenter(ModelPresenter):
    def describe_model(self):
        """
        Provide a description of the School model.
        """
        self.stream.write(
            f"Model: {self.model.__name__}. Represents schools that are part of specific paths, "
            "defining the abilities and characteristics of characters. Schools can be linked to one or more paths.\n"
        )

    def describe_instance(self, instance):
        """
        Provide a detailed single-line description of a school, including all path relations.
        """
        # General school details
        school_id = getattr(instance, "id", "unknown")
        name = getattr(instance, "name", "Unnamed")
        description = getattr(instance, "description", "No description available")
        is_default = "Yes" if getattr(instance, "is_default", False) else "No"

        # Related paths
        paths = instance.path.all()
        path_details = ", ".join(
            f"{path.id}: {path.name}" for path in paths
        )

        # Build single-line description
        line = (
            f"School ID: {school_id} -> {name} (Default: {is_default}) - "
            f"Description: {description}; Related Paths: [{path_details}]"
        )
        self.stream.write(line + "\n")


class SkillPresenter(ModelPresenter):
    def describe_model(self):
        """
        Provide a description of the Skill model.
        """
        self.stream.write(
            f"Model: {self.model.__name__}. Represents abilities tied to a school, with impacts, costs, and effects.\n"
        )

    def describe_instance(self, instance):
        """
        Provide a single-line detailed description of the skill, including all required IDs.
        """
        # General details
        skill_id = getattr(instance, "id", "unknown")
        school_id = getattr(instance, "school", None)
        if school_id:
            school_id = f"{school_id.id} ({school_id.name})"
        else:
            school_id = "unknown"
        name = getattr(instance, "name", "Unnamed")
        grade = getattr(instance, "grade", "Unknown")
        skill_type = getattr(instance, "type", "Unknown")
        description = getattr(instance, "description", "No description available")
        multi_target = "Yes" if getattr(instance, "multi_target", False) else "No"

        # Impact details
        impacts = getattr(instance, "impact", [])
        impact_details = []
        for impact in impacts:
            kind = impact.get("kind", "Unknown")
            damage_type = impact.get("type", "Unknown")
            base = impact.get("formula", {}).get("base", "Unknown")
            requirements = ", ".join(
                f"{req['stat']} >= {req['value']}" for req in impact.get("formula", {}).get("requires", [])
            )
            scaling = ", ".join(
                f"{scale['stat']} * {scale['value']}" for scale in impact.get("formula", {}).get("scaling", [])
            )
            impact_details.append(
                f"{kind} ({damage_type}, Base: {base}, Requires: {requirements}, Scaling: {scaling})"
            )

        impact_text = "; ".join(impact_details)

        # Cost details
        costs = getattr(instance, "cost", [])
        cost_details = ", ".join(f"{cost['kind']}: {cost['value']}" for cost in costs)

        # Effects
        effects = getattr(instance, "effect", [])
        effect_details = ", ".join(
            f"{effect['name']} ({effect['description']}, Chance: {effect['chance'] * 100}%)"
            for effect in effects
        )

        # Build single-line description
        line = (
            f"Skill ID: {skill_id}, School ID: {school_id} -> {name} "
            f"(Grade {grade}, Type: {skill_type}, Multi-target: {multi_target}) - "
            f"Description: {description}; Impacts: [{impact_text}]; Costs: [{cost_details}]; Effects: [{effect_details}]"
        )
        self.stream.write(line + "\n")


class ModificatorPresenter(ModelPresenter):
    def describe_model(self):
        """
        Provide a description of the Modificator model.
        """
        self.stream.write(
            f"Model: {self.model.__name__}. Represents game modificators that alter character stats or abilities.\n"
        )

    def describe_instance(self, instance):
        """
        Provide a single-line detailed description of the modificator, including associated StatModificators.
        """
        # General modificator details
        modificator_id = getattr(instance, "id", "unknown")
        name = getattr(instance, "name", "Unnamed")
        description = getattr(instance, "description", "No description available")
        icon = getattr(instance, "icon", None)
        icon_text = f"Icon: {icon.url}" if icon else "Icon: None"

        # Fetch related StatModificators
        stat_modificators = instance.statmodificator_set.all()
        stat_mod_details = []
        for stat_mod in stat_modificators:
            stat_mod_id = getattr(stat_mod, "id", "unknown")
            stat = getattr(stat_mod, "stat", "Unknown Stat")
            value = getattr(stat_mod, "value", "Unknown Value")
            stat_mod_details.append(f"{stat_mod_id}: {stat} (+{value})")

        stat_mod_text = "; ".join(stat_mod_details)

        # Build single-line description
        line = (
            f"{modificator_id}: {name} - {description} ({icon_text}); "
            f"Stat Modifiers: [{stat_mod_text}]"
        )
        self.stream.write(line + "\n")


class RankPresenter(ModelPresenter):
    def describe_model(self):
        """
        Provide a description of the Rank model.
        """
        self.stream.write(
            f"Model: {self.model.__name__}. Represents ranks that define character progression "
            "with grades, experience requirements, and potential next rank transitions.\n"
        )

    def describe_instance(self, instance):
        """
        Provide a single-line detailed description of the rank.
        """
        # General rank details
        name = getattr(instance, "name", "Unnamed Rank")
        grade = getattr(instance, "grade", "Unknown Grade")
        description = getattr(instance, "description", "No description available.")
        next_rank = getattr(instance, "next_rank", None)
        next_rank_text = next_rank.name if next_rank else "None"

        # Build single-line description in the desired format
        line = (
            f"Rank - {name} [{grade}] Description: {description} Next Rank:({next_rank_text})"
        )
        self.stream.write(line + "\n")


class ItemPresenter(ModelPresenter):
    def describe_model(self):
        """
        Provide a description of the Item model.
        """
        self.stream.write(
            f"Model: {self.model.__name__}. Represents game items with properties like type, charges, weight, and effects.\n"
        )

    def describe_instance(self, instance):
        """
        Provide a single-line detailed description of the item, including all required fields for LLM mapping.
        """
        # Core fields for LLM mapping
        item_id = getattr(instance, "id", "unknown")
        name = getattr(instance, "name", "Unnamed Item")
        description = getattr(instance, "description", "No description available")
        canonical = "Yes" if getattr(instance, "canonical", False) else "No"
        # Additional item properties
        item_type = getattr(instance, "type", "Unknown")

        # Build single-line description with all essential fields for LLM mapping
        line = (
            f"Item ID: {item_id} -> {name} (Type: {item_type}, Canonical: {canonical}) - "
            f"Description: {description};"
        )
        self.stream.write(line + "\n")


class CharacterPresenter(ModelPresenter):
    def describe_model(self):
        """
        Provide a description of the Character model.
        """
        self.stream.write(
            f"Model: {self.model.__name__}. Represents short character information like id, name, tags, "
            f"organization.id, organization.name\n"
        )

    def describe_instance(self, instance):
        """
        Provide a single-line detailed description of the character.
        """
        # Core fields for character information
        character_id = getattr(instance, "id", "unknown")
        name = getattr(instance, "name", "Unnamed Character")
        tags = getattr(instance, "tags", [])
        tags_str = ", ".join(tags) if tags else "No tags"

        # Organization information
        organization = getattr(instance, "organization", None)
        if organization:
            org_id = getattr(organization, "id", "unknown")
            org_name = getattr(organization, "name", "Unknown Organization")
            org_info = f"Organization ID: {org_id}, Name: {org_name}"
        else:
            org_info = "No organization"

        # Build single-line description
        line = (
            f"Character ID: {character_id} -> {name} (Tags: {tags_str}) - {org_info};"
        )
        self.stream.write(line + "\n")



class Serializer(PythonSerializer):
    repository = {
        "Model": ModelPresenter,
        "Skill": SkillPresenter,
        "Modificator": ModificatorPresenter,
        "School": SchoolPresenter,
        "ThePath": PathPresenter,
        "Rank": RankPresenter,
        "Item": ItemPresenter,
        "Character": CharacterPresenter,
    }
    default_presentor = ModelPresenter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream = io.StringIO()

    def start_serialization(self):
        """
        Initialize the serialization process.
        """
        if not self.stream:
            raise RuntimeError("Serializer must be initialized with a writable stream.")

    def end_serialization(self):
        """
        End the serialization process.
        """
        self.stream.write("Serialization complete.\n")

    def serialize(self, queryset, **kwargs):
        """
        Serialize a queryset or iterable of model instances.
        """
        self.stream = kwargs.pop("stream", self.stream)
        current_presentor = None
        for obj in queryset:
            model = type(obj)
            if not current_presentor or current_presentor.model != model:
                current_presentor = self.repository.get(model.__name__, self.default_presentor)(model, self.stream)
                current_presentor.describe_model()
            current_presentor.describe_instance(obj)

    def getvalue(self):
        """
        Return the serialized output as a string if the stream supports it.
        """
        pass

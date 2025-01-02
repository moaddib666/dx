from typing import List, Dict

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from typing_extensions import TypedDict

from apps.core.models import SkillTypes
from apps.core.utils.models import BaseModel
from apps.school.dto import Impact, Cost, Effect


class ThePath(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.ImageField(upload_to='icons/path/', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class School(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    path = models.ManyToManyField(ThePath,blank=True, null=True)
    icon = models.ImageField(upload_to='icons/school/', null=True, blank=True)
    is_base = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class Skill(BaseModel):
    Types = SkillTypes

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    grade = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    description = models.TextField()
    multi_target = models.BooleanField()
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='skills', null=True, blank=True)
    type = models.CharField(max_length=10, choices=Types.choices, default=Types.ATTACK)

    impact = models.JSONField(default=list, help_text='A list of dictionaries representing the impact of the skill.',
                              verbose_name='Impact', blank=False)
    cost = models.JSONField(default=list, help_text='A list of dictionaries representing the cost of the skill.',
                            verbose_name='Cost', blank=False)
    effect = models.JSONField(default=list, help_text='A list of dictionaries representing the effects of the skill.',
                              verbose_name='Effect', blank=True)

    icon = models.ImageField(upload_to='icons/skill/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'school'], name='unique_skill_name_per_school')
        ]
        ordering = ['grade', ]

    def clean(self):
        """
        Ensures that fields are either empty lists or lists of dictionaries conforming to a specified TypedDict.
        """
        super().clean()
        self.validate_json_field(self.impact, Impact, 'impact')
        self.validate_json_field(self.cost, Cost, 'cost')
        self.validate_json_field(self.effect, Effect, 'effect')

    def validate_json_field(self, field: List[Dict], field_type: TypedDict, field_name: str):
        if not isinstance(field, list):
            raise ValidationError({field_name: 'Must be a list'})

        for item in field:
            self.validate_typed_dict(item, field_type, field_name)

    def validate_typed_dict(self, item: Dict, typed_dict: TypedDict, field_name: str):
        if not isinstance(item, dict):
            raise ValidationError({field_name: 'Must be a dictionary'})

        for key, value_type in typed_dict.__annotations__.items():
            if key not in item:
                raise ValidationError({field_name: f'Missing key: {key}'})
            # FIXME: This is a hack to avoid infinite recursion
            if key == 'formula':
                # self.validate_typed_dict(item[key], value_type, field_name)
                continue
            if not isinstance(item[key], value_type):
                try:
                    item[key] = value_type(item[key])
                except ValueError as err:
                    raise ValidationError(
                        {field_name: f'Invalid type for key: {key}, expected {value_type.__name__}'}) from err

    def is_defense(self):
        return self.type == self.Types.DEFENSE

    def is_attack(self):
        return self.type == self.Types.ATTACK

    def is_buff(self):
        return self.type == self.Types.BUFF

    def is_debuff(self):
        return self.type == self.Types.DEBUFF

    def is_heal(self):
        return self.type == self.Types.HEAL

    def is_utility(self):
        return self.type == self.Types.UTILITY

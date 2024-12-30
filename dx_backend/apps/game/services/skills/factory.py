import random
import uuid

from apps.core.models import AttributeType, ImpactType, ImpactViolationType, CharacterStats
from apps.game.services.skills.base_stat_calculator import BalanceSkillCalculator
from apps.school.dto import Cost, Impact, BaseSkill, Formula, StatRequirement, Scaling
from apps.school.models import Skill


class SkillConstructor:
    """
    Base Character Attributes is 10
    --------------------------
    Charisma 10
    Concentration 10
    Flow Connection 10
    Flow Manipulation 10
    Flow Resonance 10
    Knowledge 10
    Luck 10
    Mental Strength 10
    Physical Strength 10
    Speed 10
    --------------------------
    Base Characters Stats - Based on Attributes
    Health 75
    Energy 155
    Action Points 5
    ----------------
    Cannulations fo good game experience and balance
    5 attacks to kill 75 / 5 ~= 15 Damage per turn
    5 heals to full 75 / 5 ~= 15 Health points per turn
    5 actions to kill 155 / 5 ~= 31 Energy points per action
    5 turns to kill  1 * 5 = 5 Action points per turn
    --------------------------
    1 AP ~= 15/5 ~= 3 Damage
    1 AP ~= 15/5 ~= 3 Healing
    1 AP ~= 31/5 ~= 6 Energy
    """
    model = Skill

    def __init__(self, default_grade: int = 9, calculator=BalanceSkillCalculator()):
        self.default_grade = default_grade
        self.calculator = calculator

    def _create_base_skill(self, kind: Skill.Types, school_id: uuid.UUID, cost: [Cost], impact: [Impact],
                           multi_target=False, effect=None, grade: int = None) -> BaseSkill:
        return BaseSkill(
            name="New Skill",
            description="Description of the new skill",
            school=school_id,
            multi_target=multi_target,
            type=kind,
            grade=self.default_grade or grade,
            cost=cost,
            effect=effect or [],
            impact=impact,
        )

    def _create_base_healing_skill(self, school_id: uuid.UUID, grade: int = None) -> BaseSkill:
        return self._create_base_skill(
            kind=Skill.Types.HEAL,
            school_id=school_id,
            cost=[
                Cost(
                    kind=AttributeType.ACTION_POINTS,
                    value=5
                ),
                Cost(
                    kind=AttributeType.ENERGY,
                    value=31
                )],
            impact=[
                Impact(
                    kind=ImpactType.HEAL,
                    type=ImpactViolationType.ENERGY,
                    formula=Formula(
                        base=13,
                        requires=[
                            StatRequirement(
                                stat=CharacterStats.CONCENTRATION,
                                value=10
                            )
                        ],
                        scaling=[
                            Scaling(
                                stat=CharacterStats.CONCENTRATION,
                                value=0.05
                            )
                        ]
                    ),
                ),
            ],
            grade=grade,
        )

    def _create_psychical_damage_skill(self, school_id: uuid.UUID, grade: int = None) -> BaseSkill:
        return self._create_base_skill(
            kind=Skill.Types.ATTACK,
            school_id=school_id,
            cost=[
                Cost(
                    kind=AttributeType.ACTION_POINTS,
                    value=2
                ),
                Cost(
                    kind=AttributeType.ENERGY,
                    value=12
                )],
            impact=[
                Impact(
                    kind=ImpactType.DAMAGE,
                    type=ImpactViolationType.PHYSICAL,
                    formula=Formula(
                        base=6,
                        requires=[
                            StatRequirement(
                                stat=CharacterStats.PHYSICAL_STRENGTH,
                                value=10
                            )
                        ],
                        scaling=[
                            Scaling(
                                stat=CharacterStats.FLOW_RESONANCE,
                                value=0.05
                            )
                        ]
                    ),
                ),
            ],
            grade=grade,
        )

    def _create_magic_damage_skill(self, school_id: uuid.UUID, grade: int = None,
                                   violation=ImpactViolationType.ENERGY,
                                   based_on=CharacterStats.FLOW_MANIPULATION,
                                   ) -> BaseSkill:
        return self._create_base_skill(
            kind=Skill.Types.ATTACK,
            school_id=school_id,
            cost=[
                Cost(
                    kind=AttributeType.ACTION_POINTS,
                    value=3
                ),
                Cost(
                    kind=AttributeType.ENERGY,
                    value=25
                )],
            impact=[
                Impact(
                    kind=ImpactType.DAMAGE,
                    type=violation,
                    formula=Formula(
                        base=12,
                        requires=[
                            StatRequirement(
                                stat=based_on,
                                value=10
                            )
                        ],
                        scaling=[
                            Scaling(
                                stat=based_on,
                                value=0.05
                            )
                        ]
                    ),
                ),
            ],
            grade=grade,
        )

    def _create_forbidden_magic_damage_skill(self, school_id: uuid.UUID, grade: int = None,
                                             violation=ImpactViolationType.ENERGY,
                                             based_on=CharacterStats.FLOW_RESONANCE,
                                             ) -> BaseSkill:
        return self._create_base_skill(
            kind=Skill.Types.ATTACK,
            school_id=school_id,
            cost=[
                Cost(
                    kind=AttributeType.ACTION_POINTS,
                    value=3
                ),
                Cost(
                    kind=AttributeType.ENERGY,
                    value=10
                ),
                Cost(
                    kind=AttributeType.HEALTH,
                    value=9
                )
            ],
            impact=[
                Impact(
                    kind=ImpactType.DAMAGE,
                    type=violation,
                    formula=Formula(
                        base=20,
                        requires=[
                            StatRequirement(
                                stat=based_on,
                                value=10
                            )
                        ],
                        scaling=[
                            Scaling(
                                stat=based_on,
                                value=0.05
                            )
                        ]
                    ),
                ),
            ],
            grade=grade,
        )

    def _create_random_magic_damage_skill(self, school_id: uuid.UUID, grade: int = None,
                                          violation=ImpactViolationType.ENERGY,
                                          based_on=CharacterStats.FLOW_MANIPULATION,
                                          ) -> BaseSkill:
        ap = random.randint(1, 5)
        calculated_values = self.calculator.calculate(ap=ap)
        base_skill = self._create_magic_damage_skill(school_id, grade, violation, based_on)
        base_skill["cost"][0]["value"] = ap
        base_skill["cost"][1]["value"] = calculated_values["Energy"]
        base_skill["impact"][0]["formula"]["base"] = calculated_values["Damage"]
        return base_skill

    def _create_random_forbidden_magic_damage_skill(self, school_id: uuid.UUID, grade: int = None,
                                                    violation=ImpactViolationType.ENERGY,
                                                    based_on=CharacterStats.FLOW_RESONANCE,
                                                    ) -> BaseSkill:
        ap = random.randint(1, 5)
        calculated_values = self.calculator.calculate(ap=ap)
        base_skill = self._create_forbidden_magic_damage_skill(school_id, grade, violation, based_on)
        base_skill["cost"][0]["value"] = ap
        base_skill["cost"][1]["value"] = int(calculated_values["Energy"] / 2)
        base_skill["cost"][2]["value"] = calculated_values["Damage"]
        base_skill["impact"][0]["formula"]["base"] = int(calculated_values["Damage"] * 2.1)
        return base_skill

    def _create_random_psychical_damage_skill(self, school_id: uuid.UUID, grade: int = None) -> BaseSkill:
        ap = random.randint(1, 5)
        calculated_values = self.calculator.calculate(ap=ap)
        base_skill = self._create_psychical_damage_skill(school_id, grade)
        base_skill["cost"][0]["value"] = ap
        base_skill["cost"][1]["value"] = calculated_values["Energy"]
        base_skill["impact"][0]["formula"]["base"] = calculated_values["Damage"]
        return base_skill

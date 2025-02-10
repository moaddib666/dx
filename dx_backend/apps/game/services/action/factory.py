import uuid
from functools import partial

from apps.action.models import CharacterAction, Cycle
from apps.character.models import Character
from apps.core.models import CharacterActionType, GameMasterImpactAction, AttributeType, ImpactType, \
    ImpactViolationType, CharacterStats
from apps.fight.models import FightTurnAction
from apps.game.exceptions import GameException
from apps.game.services.action.back_to_safety import BackToSafeService
from apps.game.services.action.base_service import CharacterActionServicePrototype
from apps.game.services.action.dice import DiceRollActionService
from apps.game.services.action.dimension_action import DimensionActionService
from apps.game.services.action.impact import ImpactAction
from apps.game.services.action.inspect import CharacterInspectorService
from apps.game.services.action.long_rest import CharacterLongRestService
from apps.game.services.action.move import CharacterActionPositionMoveService
from apps.game.services.action.notify import ConsoleResultNotifyService
from apps.game.services.action.player import ManualCharacterActionPlayerService
from apps.game.services.action.skill_action import SkillActionService
from apps.game.services.action.snatch import CharacterSnatchActionService
from apps.game.services.action.use_item import UseItemActionService
from apps.game.services.character.core import CharacterService
from apps.game.services.effect.facctory import ManagerEffectFactory, ApplyEffectFactory
from apps.game.services.world.auto_map import AutoMapService
from apps.game.services.world.movemant import MovementService
from apps.school.dto import Cost, Impact, Formula, StatRequirement, Scaling
from apps.school.models import School, Skill


class ActionFactory:
    pass


class FightActionFactory:
    mapping = {
        CharacterActionType.USE_SKILL: SkillActionService,
        CharacterActionType.DIMENSION_SHIFT: DimensionActionService,
    }

    def from_action(self, action: FightTurnAction):
        initiator = CharacterService(action.initiator)
        targets = [CharacterService(target) for target in action.targets.all()]
        return self.mapping[action.action_type](action, initiator, targets)


class CharacterActionFactory:
    mapping = {
        CharacterActionType.MOVE.value: CharacterActionPositionMoveService(MovementService()),
        CharacterActionType.DICE_ROLL: DiceRollActionService(),
        CharacterActionType.USE_SKILL: ImpactAction(
            ManagerEffectFactory().default(),
        ),
        CharacterActionType.USE_ITEM: UseItemActionService(ImpactAction(
            ManagerEffectFactory().default(),
        )),
        CharacterActionType.LONG_REST: CharacterLongRestService(),
        CharacterActionType.BACK_TO_SAFE_ZONE: BackToSafeService(),
        CharacterActionType.INSPECT: CharacterInspectorService(),
        CharacterActionType.SNATCH: CharacterSnatchActionService(),
    }

    def from_action(self, action: CharacterAction) -> CharacterActionServicePrototype:
        try:
            return self.mapping[action.action_type]
        except KeyError:
            raise GameException("Action not implemented")


class GameMasterActionFactory:

    def get_char(self, pk: uuid.UUID) -> Character:
        return Character.objects.get(pk=pk)

    def _construct_player_action(self, request: GameMasterImpactAction, skill: Skill) -> CharacterAction:
        initiator = self.get_char(request.initiator)
        action = CharacterAction.objects.create(
            action_type=CharacterActionType.USE_SKILL,
            initiator=initiator,
            skill=skill,
            position=initiator.position,
            cycle=Cycle.objects.current(),
        )
        targets = [self.get_char(request.target), ]
        # targets is many to many field
        action.targets.add(*targets)
        return action

    def construct_player_action(self, request: GameMasterImpactAction) -> CharacterAction:
        if request.impact_type == ImpactType.HEAL:
            skill = self.get_healing_skill()
            action = self._construct_player_action(request, skill)
            return action
        if request.impact_type == ImpactType.DAMAGE:
            action = self._construct_damage_action(request)
            return action

        raise GameException("Action not implemented")

    def _construct_damage_action(self, request: GameMasterImpactAction) -> CharacterAction:
        initiator = self.get_char(request.initiator)
        action = CharacterAction.objects.create(
            action_type=CharacterActionType.USE_SKILL,
            initiator=initiator,
            skill=self.get_damage_skill(request.impact_violation),
            position=initiator.position,
            cycle=Cycle.objects.current(),
        )
        targets = [self.get_char(request.target), ]
        # targets is many to many field
        action.targets.add(*targets)
        return action

    def get_damage_skill(self, violation: ImpactViolationType) -> Skill:
        if violation == ImpactViolationType.NONE:
            const = [
                Cost(
                    kind=AttributeType.ACTION_POINTS,
                    value=3
                ),
                Cost(
                    kind=AttributeType.ENERGY,
                    value=10
                )
            ]
            impact = []
        elif violation != ImpactViolationType.PHYSICAL:
            # Magical damage from mages
            const = [
                Cost(
                    kind=AttributeType.ACTION_POINTS,
                    value=4
                ),
                Cost(
                    kind=AttributeType.ENERGY,
                    value=15
                )
            ]
            impact = [
                Impact(
                    kind=ImpactType.DAMAGE,
                    type=violation,
                    formula=Formula(
                        base=15,
                        requires=[
                            StatRequirement(
                                stat=CharacterStats.FLOW_MANIPULATION,
                                value=10
                            )
                        ],
                        scaling=[
                            Scaling(
                                stat=CharacterStats.FLOW_MANIPULATION,
                                value=0.2
                            ),
                            Scaling(
                                stat=CharacterStats.FLOW_RESONANCE,
                                value=0.2
                            ),
                            Scaling(
                                stat=CharacterStats.FLOW_CONNECTION,
                                value=0.2
                            ),
                        ]
                    ),
                )
            ]
        else:
            # Physical damage from warriors
            const = [
                Cost(
                    kind=AttributeType.ACTION_POINTS,
                    value=5
                ),
                Cost(
                    kind=AttributeType.ENERGY,
                    value=20
                )
            ]
            impact = [
                Impact(
                    kind=ImpactType.DAMAGE,
                    type=violation,
                    formula=Formula(
                        base=10,
                        requires=[
                            StatRequirement(
                                stat=CharacterStats.PHYSICAL_STRENGTH,
                                value=10
                            )
                        ],
                        scaling=[
                            Scaling(
                                stat=CharacterStats.PHYSICAL_STRENGTH,
                                value=0.2
                            ),
                            Scaling(
                                stat=CharacterStats.SPEED,
                                value=0.1
                            ),
                            Scaling(
                                stat=CharacterStats.FLOW_RESONANCE,
                                value=0.1
                            ),
                        ]
                    ),
                )
            ]

        s, _ = Skill.objects.get_or_create(
            name=f"Damage {violation} grade 9",
            defaults=dict(
                description="Damage skill",
                school=self.get_gm_school(),
                multi_target=False,
                type=Skill.Types.ATTACK,
                grade=9,
                cost=const,
                effect=[],
                impact=impact,
            )
        )
        return s

    def get_healing_skill(self) -> Skill:
        s, _ = Skill.objects.get_or_create(
            name="Healing",
            description="Healing skill",
            school=self.get_gm_school(),
            multi_target=False,
            type=Skill.Types.HEAL,
            grade=9,
            cost=[
                Cost(
                    kind=AttributeType.ACTION_POINTS,
                    value=7
                ),
                Cost(
                    kind=AttributeType.ENERGY,
                    value=10
                )],
            effect=[],
            impact=[
                Impact(
                    kind=ImpactType.HEAL,
                    type=ImpactViolationType.PHYSICAL,
                    formula=Formula(
                        base=15,
                        requires=[
                            StatRequirement(
                                stat=CharacterStats.FLOW_MANIPULATION,
                                value=10
                            )
                        ],
                        scaling=[
                            Scaling(
                                stat=CharacterStats.FLOW_MANIPULATION,
                                value=0.2
                            )
                        ]
                    ),
                ),
            ],
        )
        return s

    def get_gm_school(self) -> School:
        s, _ = School.objects.get_or_create(
            name="Game Master",
            description="The school for Game Masters",
        )
        return s


ManualCharacterActionPlayerServiceFactory = partial(
    ManualCharacterActionPlayerService,
    notify_svc=ConsoleResultNotifyService(),
    effects_manager_factory=ManagerEffectFactory(),
    effects_apply_factory=ApplyEffectFactory(),
    auto_map_svc=AutoMapService(),
)

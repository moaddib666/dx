import logging
import uuid
from datetime import timedelta

from django.utils import timezone

from apps.game.dto.impact import CalculatedImpact
from apps.game.exceptions import GameLogicException
from apps.player.models import Player
from apps.school.models import Skill
from apps.world.models import Dimension


class PlayerService:
    logger = logging.getLogger("game.services.player")

    def __init__(self, player: Player):
        self.player = player

    def get_max_ap(self):
        return int(round(self.player.stats.speed * 0.5 * self.player.dimension.speed))

    def get_player_info(self):
        self.player.refresh_from_db()
        return {
            'id': self.player.id,
            'name': self.player.name,
            'stats': {
                'health': self.player.current_health_points,
                'max_health': self.player.stats.health_points,
                'energy': self.player.current_energy_points,
                'max_energy': self.player.stats.energy_points,
                'ap': self.player.current_active_points,
                'max_ap': self.get_max_ap(),
            },
            'location': {
                'id': self.player.current_location.id,
                'name': self.player.current_location.name,
            },
            "dimension": {
                "number": self.player.dimension.id,
                "speed": self.player.dimension.speed,
                "energy": self.player.dimension.energy,
            },
            'rank': {
                'name': self.player.rank.name,
                'experience': self.player.experience,
                'grade': self.player.rank.grade,
                'next_rank_experience': self.player.rank.next_rank.experience_needed,
            },
            'skills': self.player.learned_skills.values_list('skill__id', flat=True),
            'schools': self.player.learned_schools.values_list('school__id', flat=True),
            'path': self.player.path.id if self.player.path else None,
            'active_effects': [],
            'fight': self.player.fight_id,
            'duel_invitations': self.player.duel_invitations_received.exclude(
                is_accepted=True, is_rejected=True, created_at__gte=timezone.now() - timedelta(minutes=5)
            ).values_list('id', flat=True),
        }

    def notify(self, message: dict):
        self.logger.info(f"Sending notification to {self.player.name}: {message}")

    def chose_path(self, path):
        if self.player.path:
            raise GameLogicException("Player already chose a path")
        if self.player.rank.grade == 0:
            raise GameLogicException("Player must reach rank 1 to choose a path")
        self.player.path = path
        self.player.save()

    def has_skill(self, skill_id: uuid.UUID):
        try:
            self.player.learned_skills.get(skill_id=skill_id)
        except Skill.DoesNotExist:
            raise GameLogicException("Player does not have skill")

    def get_current_speed(self) -> float:
        return self.player.stats.speed * self.player.dimension.speed

    def get_stat(self, param: str) -> int:
        pretty_stat = param.replace(" ", "_").lower()
        return getattr(self.player.stats, pretty_stat, 0)

    def impacted(self, calculated_impact: CalculatedImpact):
        self.logger.debug(f"Player {self.player.id} impacted with {calculated_impact}")
        if self.player.current_health_points <= 0:
            self.logger.debug(f"Player {self.player.id} is already dead")
            return
        if calculated_impact['kind'] == "Damage":
            self.player.current_health_points -= calculated_impact['value']
            self.player.save()
            self.logger.info(f"Player {self.player.id} received {calculated_impact['value']} of {calculated_impact['kind']} damage")
        else:
            raise GameLogicException("Unknown impact kind")

    def refill_ap(self):
        self.player.current_active_points = self.get_max_ap()
        self.player.save()

    def refill_energy(self):
        self.player.current_energy_points = self.player.stats.energy_points
        self.player.save()

    def refill_health(self):
        self.player.current_health_points = self.player.stats.health_points
        self.player.save()

    def dimension_shift(self, target_dimension: Dimension):
        self.player.dimension = target_dimension
        self.player.save()

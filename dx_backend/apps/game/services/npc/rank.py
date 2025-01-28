from apps.character.models import Rank
from .stats import StatsApplier


class NpcRankService:

    def __init__(self, applier: StatsApplier):
        self.applier = applier

    def rank_npc(self, npc, grade: int, grade_rank: int):
        current_ncp_rank = npc.rank
        new_npc_rank = Rank.objects.get(grade=grade, grade_rank=grade_rank)
        spent_skill_points = Rank.objects.get_skill_points(current_ncp_rank.grade, new_npc_rank.grade)
        self.applier.spend_stat_points(npc, spent_skill_points)
        npc.rank = new_npc_rank
        npc.experience = new_npc_rank.experience_needed + 1
        npc.save(
            update_fields=['rank', 'experience']
        )

from apps.core.models import BriefPlayerInfo
from apps.game.services.player.core import PlayerService
from apps.player.models import Player


def get_brief_info(p: Player) -> BriefPlayerInfo:
    svc = PlayerService(p)
    return svc.get_brief_info()


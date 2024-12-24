from apps.core.models import BriefCharacterInfo
from apps.game.services.character.core import CharacterService
from apps.character.models import Character


def get_brief_info(p: Character) -> BriefCharacterInfo:
    svc = CharacterService(p)
    return svc.get_brief_info()


# This file will import all admin classes from the module files
# to maintain the same functionality as the original admin.py file

from .biography import CharacterBiographyAdmin
from .character import CharacterAdmin, CharacterBiographyInline
from .filters import SubLocationFilter, GridZFilter
from .follow_rule import FollowRuleAdmin
from .forms import BulkChangeAvatarForm, BulkChangeOrganizationForm
from .inlines import (
    StatInline, StatModifierInline, OwnedItemsInline,
    LearnedSchoolsInline, LearnedSkillsInline,
    ActiveEffectsInline, ActiveShieldsInline
)
from .npc import (
    CharacterTemplateAdmin, CharacterStatsTemplateAdmin, CharacterBiographyTemplateAdmin,
    CharacterStatTemplateInline, CharacterSkillTemplateInline, CharacterSchoolTemplateInline,
    CharacterModifierTemplateInline, CharacterEquipmentTemplateInline, CharacterNameTemplateInline
)
from .organization import OrganizationAdmin
from .published_character import PublishedCharacterAdmin
from .rank import RankAdmin
from .relation import OrganizationRelationAdmin, CharacterRelationAdmin
from .stat import StatAdmin

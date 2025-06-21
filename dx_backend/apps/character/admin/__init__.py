# This file will import all admin classes from the module files
# to maintain the same functionality as the original admin.py file

from .forms import BulkChangeAvatarForm, BulkChangeOrganizationForm
from .filters import SubLocationFilter, GridZFilter
from .organization import OrganizationAdmin
from .rank import RankAdmin
from .character import CharacterAdmin, CharacterBiographyInline
from .inlines import (
    StatInline, StatModifierInline, OwnedItemsInline, 
    LearnedSchoolsInline, LearnedSkillsInline, 
    ActiveEffectsInline, ActiveShieldsInline
)
from .stat import StatAdmin
from .biography import CharacterBiographyAdmin
from .npc import (
    CharacterTemplateAdmin, CharacterStatsTemplateAdmin, CharacterBiographyTemplateAdmin,
    CharacterStatTemplateInline, CharacterSkillTemplateInline, CharacterSchoolTemplateInline,
    CharacterModifierTemplateInline, CharacterEquipmentTemplateInline, CharacterNameTemplateInline
)

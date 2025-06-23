# Campaign Field Strategy - Django Model Analysis

## Executive Summary

We need to provide campaign feature so that Players and Game Masters can only interact with objects that belong to the
same campaign.

- **Game Masters** can interact with all objects in the campaign. not objects from other campaigns. the comparing of
  game master is the campaign og his main character.
- **Players** can only interact with objects that belong to the same campaign as their main character.
- **Campaign** is a core game concept that should be implemented in the database schema to allow different groups of
  players to play in the same game world without interfering with each other.
- The campaign field should be added to all models that are relevant to the campaign context, allowing for filtering and
  access control based on the campaign.
- The campaign field should be a foreign key to the `game.Campaign` model, which represents the campaign entity.
- The migration must be created by creating new campaign if it does and automatically assigning it to all existing
  objects in the database to first campaign.

## Core Principle: Inheritance Over Duplication

Since `core.GameObject` is already a polymorphic root with a campaign field, its children should inherit campaign
context rather than duplicate the field.

---

## 🎯 REQUIRED Campaign Fields (18 models)

### Polymorphic Root Models

- ✅ **`core.GameObject`** (already has campaign) - Polymorphic root
- ✅ **`core.StatObject`** - Polymorphic root (if used)
- ✅ **`core.ViolationObject`** - Polymorphic root (if used)

### Campaign Configuration Models

- ✅ **`game.Campaign`** - This IS the campaign entity
- ✅ **`character.CharacterTemplate`** (already has campaign)
- 🔧 **`world.Dimension`** - World configuration campaign-specific
- ✅ **`character.Organization`** - Organizations are campaign-specific
- ✅  **`school.ThePath`** - Spiritual paths are game common
- ✅  **`character.Rank`** - Rank systems are game common
- 🔧 **`school.School`** - Schools are campaign-specific
- 🔧 **`school.Skill`** - Skills are campaign-specific
- 🔧 **`items.Item`** - Item templates are campaign-specific
- 🔧 **`effects.Effect`** - Effect templates are campaign-specific
- 🔧 **`shields.Shield`** - Shield templates are campaign-specific
- 🔧 **`modificators.Modificator`** - Modificator templates are campaign-specific
- 🔧 **`currency.CurrencyToken`** - Currency types are campaign-specific

### World Geography Models

- 🔧 **`world.Planet`** - Top-level world structure
- 🔧 **`world.Map`** - Maps are campaign-specific

---

### Character-Related Models (filter via character.campaign)

- ❌ **`character.CharacterBiography`** - Access via `character.campaign`
- ❌ **`character.Stat`** - Access via `character.campaign`
- ❌ **`character.StatModifier`** - Access via `character.campaign`
- ❌ **`character.CharacterRelation`** - Both characters have campaign context
- ❌ **`character.FollowRule`** - Both leader/follower have campaign context
- ❌ **`skills.LearnedSkill`** - Access via `character.campaign`
- ❌ **`skills.LearnedSchool`** - Access via `character.campaign`
- ❌ **`items.CharacterItem`** - Access via `character.campaign`
- ❌ **`modificators.CharacterModificator`** - Access via `character.campaign`
- ❌ **`currency.CharacterCurrency`** - Access via `character.campaign`
- ❌ **`effects.ActiveEffect`** - Access via `target.campaign`
- ❌ **`shields.ActiveShield`** - Access via `target.campaign`
- ❌ **`game.Session`** - Access via `character.campaign`

### Action System Models (filter via character/position context)

- ✅ **`action.Cycle`** - Core Game Element must have campaign
- ✅ **`action.CharacterAction`** - Core Game Element must have campaign
- ❌ **`action.ActionImpact`** - Access via `action.initiator.campaign`
- ❌ **`action.DiceRollResult`** - Access via action chain

### Template Sub-Models (filter via parent template)

- ❌ **`character.CharacterStatsTemplate`** - Access via `charactertemplate.campaign`
- ❌ **`character.CharacterStatTemplate`** - Access via template chain
- ❌ **`character.CharacterBiographyTemplate`** - Access via `charactertemplate.campaign`
- ❌ **`character.CharacterSkillTemplate`** - Access via `template.campaign`
- ❌ **`character.CharacterSchoolTemplate`** - Access via `template.campaign`
- ❌ **`character.CharacterModifierTemplate`** - Access via `template.campaign`
- ❌ **`character.CharacterEquipmentTemplate`** - Access via `template.campaign`
- ❌ **`character.CharacterNameTemplate`** - Access via `template.campaign`

---

## 🌍 WORLD MODELS Strategy

### Hierarchical Campaign Inheritance

World models should inherit campaign context hierarchically:

```
world.Dimension (must have campaign)
world.Planet (must have campaign)
└── world.Continent (must have campaign)
    └── world.Country (must have campaign)
        └── world.City (must have campaign)
            └── world.Area ((must have campaign)
                └── world.Location (must have campaign)
                    └── world.SubLocation (must have campaign)
                        └── world.Position (take campaign from parent sublocation.campaign)
                            └── world.PositionConnection (take campaign from position_from.dimension.campaign)
```

### Special Cases

- ❌ **`world.PositionConnection`** - Access via `position_from.dimension.campaign`
- ❌ **`world.MapPosition`** - Access via `map.campaign`
- ❌ **`bargain.Bargain`** - Access via `side_a.campaign` or `side_b.campaign`
- ❌ **`bargain.OfferedItem`** - Access via `bargain` chain
- ❌ **`character.OrganizationRelation`** - Access via organization campaigns
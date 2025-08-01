# Sandbox Fixture Guide

## Overview

The `fixtures/test/sandbox.yaml` file contains comprehensive test data for all Django models tagged with
`TagsDescriptor.BaseTags.SANDBOX` in the DX Backend application. This fixture provides a complete sandbox environment
for testing game mechanics, character systems, world data, and other core functionality.

## Generation Command

This fixture was generated using the Django management command:

```bash
python manage.py dumpdata character.CharacterBiographyTemplate character.CharacterEquipmentTemplate character.CharacterModifierTemplate character.CharacterNameTemplate character.CharacterSchoolTemplate character.CharacterSkillTemplate character.CharacterStatTemplate character.CharacterStatsTemplate character.CharacterTemplate character.Organization character.Rank core.StatObject core.ViolationObject currency.CurrencyToken effects.Effect items.Item modificators.Modificator school.School school.Skill school.ThePath shields.Shield world.Area world.City world.Continent world.Country world.Dimension world.Location world.Planet world.Position world.PositionConnection world.SubLocation --format yaml -o fixtures/test/sandbox.yaml
```

## Model Categories

### Character Models (9 models)

- `character.CharacterBiographyTemplate` - Character biography templates with background stories, appearances, and
  variations
- `character.CharacterEquipmentTemplate` - Equipment loadout templates for characters
- `character.CharacterModifierTemplate` - Character stat and ability modifiers
- `character.CharacterNameTemplate` - Name generation templates
- `character.CharacterSchoolTemplate` - School/class associations for characters
- `character.CharacterSkillTemplate` - Skill templates and progressions
- `character.CharacterStatTemplate` - Base stat templates
- `character.CharacterStatsTemplate` - Complete stat block templates
- `character.CharacterTemplate` - Master character templates
- `character.Organization` - Organizations and factions
- `character.Rank` - Ranking systems within organizations

### World Models (11 models)

- `world.Dimension` - Dimensional planes and realms
- `world.Planet` - Planetary bodies within dimensions
- `world.Continent` - Continental landmasses
- `world.Country` - Nations and territories
- `world.Area` - Regional areas within countries
- `world.City` - Urban settlements
- `world.Location` - Specific locations and points of interest
- `world.Position` - Coordinate positions in the world
- `world.PositionConnection` - Connections between positions
- `world.SubLocation` - Sub-areas within locations

### Core Models (2 models)

- `core.StatObject` - Core statistical objects and definitions
- `core.ViolationObject` - Rule violation tracking objects

### Game Content Models (9 models)

- `school.School` - Magic schools and disciplines
- `school.Skill` - Individual skills and abilities
- `school.ThePath` - Character progression paths
- `shields.Shield` - Defensive equipment
- `effects.Effect` - Magical and mechanical effects
- `items.Item` - Game items and equipment
- `modificators.Modificator` - Stat and ability modifiers
- `currency.CurrencyToken` - In-game currency systems

## Data Structure

Each fixture entry follows Django's standard format:

```yaml
- model: app_name.ModelName
  pk: uuid-primary-key
  fields:
    field_name: field_value
    created_at: timestamp
    updated_at: timestamp
    # ... other model fields
```

## Usage in Tests

### Loading the Fixture

#### Method 1: Django TestCase with fixtures

```python
from django.test import TestCase


class MyGameTest(TestCase):
    fixtures = ['fixtures/test/sandbox.yaml']

    def test_character_creation(self):
        from apps.character.models import CharacterTemplate
        # All sandbox character templates are now available
        templates = CharacterTemplate.objects.all()
        self.assertGreater(templates.count(), 0)
```

#### Method 2: Using Django's loaddata command

```bash
# Load fixture data into test database
python manage.py loaddata fixtures/test/sandbox.yaml
```

#### Method 3: Programmatic loading in tests

```python
from django.core.management import call_command
from django.test import TestCase


class MyGameTest(TestCase):
    def setUp(self):
        call_command('loaddata', 'fixtures/test/sandbox.yaml')

    def test_world_data(self):
        from apps.world.models import Dimension
        dimensions = Dimension.objects.all()
        self.assertGreater(dimensions.count(), 0)
```

### Common Test Patterns

#### Testing Character Systems

```python
def test_character_template_system(self):
    from apps.character.models import CharacterTemplate, CharacterBiographyTemplate

    # Test character template creation
    char_template = CharacterTemplate.objects.first()
    self.assertIsNotNone(char_template)

    # Test biography templates
    bio_templates = CharacterBiographyTemplate.objects.all()
    self.assertGreater(bio_templates.count(), 0)
```

#### Testing World Navigation

```python
def test_world_structure(self):
    from apps.world.models import Dimension, Planet, Country

    # Test dimensional structure
    dimensions = Dimension.objects.all()
    planets = Planet.objects.all()
    countries = Country.objects.all()

    self.assertGreater(dimensions.count(), 0)
    self.assertGreater(planets.count(), 0)
    self.assertGreater(countries.count(), 0)
```

#### Testing Game Mechanics

```python
def test_game_content(self):
    from apps.school.models import School, Skill
    from apps.items.models import Item
    from apps.effects.models import Effect

    # Test schools and skills
    schools = School.objects.all()
    skills = Skill.objects.all()

    # Test items and effects
    items = Item.objects.all()
    effects = Effect.objects.all()

    self.assertGreater(schools.count(), 0)
    self.assertGreater(skills.count(), 0)
    self.assertGreater(items.count(), 0)
    self.assertGreater(effects.count(), 0)
```

## Benefits for Testing

### Complete Game Environment

- Provides a full sandbox environment with interconnected game data
- Includes character templates, world locations, items, skills, and effects
- Enables testing of complex game mechanics and interactions

### Consistent Test Data

- All tests use the same baseline data set
- Reproducible test results across different environments
- No need to create test data manually in each test

### Performance Benefits

- Pre-generated data loads faster than creating objects in setUp methods
- Reduces test execution time for integration tests
- Enables testing with realistic data volumes

### Comprehensive Coverage

- Tests can verify relationships between different model types
- Enables end-to-end testing of game workflows
- Supports testing of complex queries and data interactions

## Maintenance

### Updating the Fixture

To regenerate the fixture with current sandbox data:

```bash
python manage.py dumpdata character.CharacterBiographyTemplate character.CharacterEquipmentTemplate character.CharacterModifierTemplate character.CharacterNameTemplate character.CharacterSchoolTemplate character.CharacterSkillTemplate character.CharacterStatTemplate character.CharacterStatsTemplate character.CharacterTemplate character.Organization character.Rank core.StatObject core.ViolationObject currency.CurrencyToken effects.Effect items.Item modificators.Modificator school.School school.Skill school.ThePath shields.Shield world.Area world.City world.Continent world.Country world.Dimension world.Location world.Planet world.Position world.PositionConnection world.SubLocation --format yaml -o fixtures/test/sandbox.yaml
```

### Finding Sandbox Models

Use the helper script to identify all SANDBOX-tagged models:

```bash
python hacking/map_sandbox_models.py
```

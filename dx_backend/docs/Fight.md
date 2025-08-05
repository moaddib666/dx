# Fight System Documentation

## Overview

The DX Game World implements a sophisticated turn-based fight system that manages combat between characters across
multiple cycles. The system handles fight detection, character joining/leaving, and fight resolution through a
coordinated set of services.

## Architecture Overview

The fight system is built around several key components:

1. **Models**: Core data structures for fights and pending participants
2. **Services**: Specialized classes handling different aspects of fight management
3. **Coordinator**: Orchestrates all fight services in the correct order
4. **Integration**: Hooks into the main game loop

## Core Models

### Fight Model

**Location**: `apps/fight/models.py:6-41`

```python
class Fight(BaseModel):
    campaign = models.ForeignKey('game.Campaign', on_delete=models.CASCADE, related_name='fights')
    position = models.ForeignKey('world.Position', on_delete=models.CASCADE, related_name='fights')
    attacker = models.ForeignKey('character.Character', on_delete=models.CASCADE, related_name='fights_initiated')
    defender = models.ForeignKey('character.Character', on_delete=models.CASCADE, related_name='fights_attacked')

    duel = models.BooleanField(default=False)
    current_round = models.PositiveIntegerField(default=1)
    open = models.BooleanField(default=True)

    created = models.ForeignKey('action.Cycle', on_delete=models.CASCADE, related_name='fights_started')
    ended_at = models.ForeignKey('action.Cycle', on_delete=models.CASCADE, related_name='fights_ended', null=True)
```

**Key Relationships**:

- **Campaign**: Every fight belongs to a specific campaign
- **Position**: Fight location in the world
- **Attacker/Defender**: Initial fight participants
- **Created/Ended_at**: Lifecycle tracking via Cycles

### CharactersPendingJoinFight Model

**Location**: `apps/fight/models.py:43-67`

```python
class CharactersPendingJoinFight(BaseModel):
    character = models.ForeignKey('character.Character', on_delete=models.CASCADE, related_name='pending_fights')
    fight = models.ForeignKey(Fight, on_delete=models.CASCADE, related_name='pending_joiners')
    cycle = models.ForeignKey('action.Cycle', on_delete=models.CASCADE, related_name='pending_join_fights')
```

**Purpose**: Implements the 1-cycle delay mechanism for joining fights. Characters must wait one cycle before becoming
active participants.

### Character Model Fight Integration

**Location**: `apps/character/models/player.py:104`

```python
fight = models.ForeignKey('fight.Fight', on_delete=models.SET_NULL, null=True, blank=True, related_name='joined')
```

**Key Relationships**:

- **Character.fight**: Direct reference to current fight (null if not fighting)
- **Character.pending_fights**: M2M relationship through CharactersPendingJoinFight

## Service Architecture

### 1. FightDetector

**Location**: `apps/game/services/fight/detector.py`

**Purpose**: Detects aggressive actions that should create new fights.

**Key Methods**:

- `detect_fights(cycle)`: Main entry point for fight detection
- `_get_aggressive_actions(previous_cycle)`: Finds aggressive actions from previous cycle
- `_should_create_fight(action)`: Determines if action should trigger fight creation
- `_create_fight_from_action(action, cycle)`: Creates Fight instance

**Logic Flow**:

1. Gets aggressive actions from previous cycle (not already in fights)
2. Checks if actions have aggressive impacts (DAMAGE, etc.) or are START_FIGHT actions
3. Validates participants are still active and at the same position
4. Creates Fight with attacker (action initiator) and defender (first target)
5. Emits FightStarted event

**Code Reference**: `apps/game/services/fight/detector.py:32-59`

### 2. FightAutoJoiner

**Location**: `apps/game/services/fight/auto_joiner.py`

**Purpose**: Automatically adds characters at fight positions to pending joiners.

**Key Methods**:

- `process_auto_joins(cycle)`: Processes all active fights for auto-joining
- `_find_potential_joiners(fight)`: Finds characters at fight position not in fight
- `_add_to_pending_join(fight, character, cycle)`: Adds character to pending joiners

**Logic Flow**:

1. Finds all active fights in campaign
2. For each fight, identifies characters at same position not already fighting
3. Checks character viability (active, has health, not incapacitated)
4. Adds viable characters to CharactersPendingJoinFight with current cycle
5. Sets character.fight reference and spends all AP
6. Emits pending join events

**Code Reference**: `apps/game/services/fight/auto_joiner.py:31-71`

### 3. FightPendingJoiner

**Location**: `apps/game/services/fight/pending_joiner.py`

**Purpose**: Converts pending joiners to active participants after 1-cycle delay.

**Key Methods**:

- `process_pending_joiners(cycle)`: Processes all pending joiners ready to join
- `_should_join_fight(fight, character)`: Validates character can still join
- `_convert_to_active_participant(fight, character, pending_record)`: Activates participant

**Logic Flow**:

1. Finds CharactersPendingJoinFight records from previous cycles (1-cycle delay)
2. Validates fight is still open and character is still viable
3. Removes pending record and confirms character.fight reference
4. Spends all character AP
5. Emits join events

**Code Reference**: `apps/game/services/fight/pending_joiner.py:28-85`

### 4. FightAutoLeaver

**Location**: `apps/game/services/fight/auto_leaver.py`

**Purpose**: Removes characters who should no longer be in fights.

**Key Methods**:

- `process_auto_leave(cycle)`: Processes all fights for character removal
- `_should_character_leave(fight, character)`: Determines if character should leave
- `_remove_participant(fight, character)`: Removes character from fight

**Logic Flow**:

1. Checks all fight participants (active and pending)
2. Identifies characters who changed position or became inactive
3. Removes character.fight reference and deletes pending records
4. Emits leave events

**Code Reference**: `apps/game/services/fight/auto_leaver.py:28-63`

### 5. FightCloser

**Location**: `apps/game/services/fight/fight_closer.py`

**Purpose**: Determines when fights should end and closes them.

**Key Methods**:

- `process_fight_endings(cycle)`: Processes all active fights for closure
- `_should_close_fight(fight, cycle)`: Determines if fight should close
- `_has_viable_participants(fight)`: Checks if enough viable participants remain
- `_is_fight_inactive(fight, cycle)`: Checks for 2 cycles without aggressive actions

**Logic Flow**:

1. Evaluates all active fights for closure conditions:
    - Less than 2 viable participants
    - No aggressive actions for 2+ cycles
    - No participants at fight position
2. Sets fight.open = False and fight.ended_at = current_cycle
3. Clears all Character.fight references
4. Deletes all CharactersPendingJoinFight records
5. Emits FightEnded event

**Code Reference**: `apps/game/services/fight/fight_closer.py:33-50`

### 6. FightCoordinator

**Location**: `apps/game/services/fight/coordinator.py`

**Purpose**: Orchestrates all fight services in correct execution order.

**Key Methods**:

- `process_all_fights()`: Executes all fight services in proper sequence

**Execution Order**:

1. **FightDetector**: Create new fights from aggressive actions
2. **FightAutoLeaver**: Remove characters who shouldn't be in fights
3. **FightPendingJoiner**: Convert pending joiners to active participants
4. **FightAutoJoiner**: Add new characters to pending joiners
5. **FightCloser**: Close fights that should end

**Code Reference**: `apps/game/services/fight/coordinator.py:39-83`

## Complete Fight Flow

### Phase 1: Fight Initiation

```
Cycle N: Aggressive Action (USE_SKILL with DAMAGE impact)
- Action performed and marked as performed=True
-> No fight created yet (happens in next cycle)

Cycle N+1: Fight Detection
- FightDetector.detect_fights() runs
- Finds aggressive action from Cycle N
- Creates Fight(attacker=initiator, defender=target, position=action.position)
- Fight.open=True, Fight.created=Cycle N+1
-> Emits FightStarted event
```

### Phase 2: Character Auto-Joining

```
Cycle N+1: Same cycle as fight creation
- FightAutoJoiner.process_auto_joins() runs
- Finds characters at fight.position not in fight
- Creates CharactersPendingJoinFight(character, fight, cycle=N+1)
- Sets character.fight = fight
- Spends all character AP (current_active_points = 0)
-> Emits PendingJoinFight events
```

### Phase 3: Pending Joiner Activation (1-Cycle Delay)

```
Cycle N+2: Pending joiner processing
- FightPendingJoiner.process_pending_joiners() runs
- Finds CharactersPendingJoinFight records from Cycle N+1
- Validates characters still viable for fighting
- Deletes CharactersPendingJoinFight records
- Confirms character.fight references
-> Emits CharacterJoinFight events
```

### Phase 4: Active Fighting

```
Cycle N+2 onwards: Active fight phase
- Characters in fight.joined can perform fight actions
- Actions have fight=fight_id set
- New characters arriving at position auto-join as pending
- FightAutoLeaver removes characters who leave position
-> Fight continues until closure conditions met
```

### Phase 5: Fight Closure

```
Fight Closure Triggers:
- Less than 2 viable participants
- No aggressive actions for 2+ cycles
-> No participants at fight position

Closure Process:
- FightCloser.process_fight_endings() runs
- Sets fight.open=False, fight.ended_at=current_cycle
- Character.objects.filter(fight=fight).update(fight=None)
- CharactersPendingJoinFight.objects.filter(fight=fight).delete()
-> Emits FightEnded event
```

## Integration with Game Loop

### ManualCharacterActionPlayerService Integration

**Location**: `apps/game/services/fight/integration.py`

The fight system integrates into the main game loop via `FightGameLoopIntegration`:

**prepare_cycle_fights()**: Called during ManualCharacterActionPlayerService.prepare()

- Runs FightCoordinator.process_all_fights()
- Processes all fight lifecycle management

**post_cycle_fights()**: Called during ManualCharacterActionPlayerService.post()

- Currently placeholder for post-cycle fight processing

## Key Data Flows

### Character State Transitions

```
Not Fighting
    � (arrives at fight position)
Pending Joiner (CharactersPendingJoinFight record created)
    � (1 cycle delay)
Active Participant (Character.fight set)
    � (leaves position or fight ends)
Not Fighting (Character.fight = null)
```

### Fight State Transitions

```
Non-existent
    � (aggressive action detected)
Created (Fight.open=True)
    � (closure conditions met)
Ended (Fight.open=False, Fight.ended_at set)
```

## Testing Patterns

### Key Test Scenarios (from fight.py test)

**Location**: `apps/game/tests/unit/fight.py:62-325`

1. **Fight Creation**: Aggressive NPC attacks character � fight created next cycle
2. **Auto-Join**: Characters at fight position become pending joiners
3. **Pending Processing**: 1-cycle delay before joining as active participants
4. **Fight Actions**: Only active participants can perform fight actions
5. **Fight Closure**: Ends after 2 cycles without aggressive actions

### Test Assertions Pattern

```python
# Fight creation verification
self.assertTrue(npc_1.fight, "NPC should be in fight")
self.assertEqual(npc_1.fight, character1.fight, "Should be in same fight")
self.assertEqual(fight.attacker, npc_1, "NPC must be attacker")

# Pending joiner verification
self.assertTrue(character2.pending_fights.exists(), "Should have pending fight")
self.assertEqual(character2.current_active_points, 0, "Should have 0 AP")

# Fight closure verification  
self.assertTrue(fight.ended_at, "Fight should be ended")
self.assertFalse(character1.fight, "Should not be in fight after closure")
```

## Error Handling and Edge Cases

### Character Viability Checks

- **Health**: Must have current_health_points > 0
- **Active Status**: Must have is_active = True
- **Position**: Must be at fight.position
- **Incapacitation**: Cannot have KNOCKED_OUT, COMA, SLEEPING, PARALYZED effects

### Fight Closure Conditions

- **Viable Participants**: Need at least 2 characters capable of fighting
- **Activity**: Must have aggressive actions within last 2 cycles
- **Position Presence**: At least one participant must remain at fight.position

### Race Condition Prevention

- **1-Cycle Delay**: Prevents immediate joining conflicts
- **AP Spending**: Ensures characters can't act immediately after joining
- **Ordered Processing**: FightCoordinator ensures services run in correct sequence

## Events and Notifications

### Fight Lifecycle Events

- **FightStartedEvent**: Emitted when fight is created
- **CharacterPendingJoinFightEvent**: Character becomes pending joiner
- **PendingJoinFightEvent**: Sent to specific character
- **CharacterJoinFightEvent**: Character becomes active participant
- **JoinedFightEvent**: Sent to specific character
- **CharacterLeaveFightEvent**: Character leaves fight
- **LeftFightEvent**: Sent to specific character
- **FightEndedEvent**: Fight is closed

### Event Broadcasting

All events are published via `notifier.bus.publish(event)` and broadcast to relevant characters at the fight position.

## Performance Considerations

### Query Optimization

- **Prefetch Related**: Services use `select_related()` and `prefetch_related()`
- **Bulk Updates**: Character.objects.filter(fight=fight).update(fight=None)
- **Filtered Queries**: Only process active fights and viable characters

### Scalability Notes

- Fight system processes all fights in campaign each cycle
- Could be optimized for large campaigns with many simultaneous fights
- Event system allows for real-time updates without polling

## Summary

The DX fight system implements a sophisticated turn-based combat mechanism with the following key features:

1. **Automatic Fight Detection**: Based on aggressive actions from previous cycles
2. **Position-Based Auto-Joining**: Characters automatically join fights at their location
3. **1-Cycle Delay Mechanism**: Prevents immediate joining conflicts
4. **Comprehensive State Management**: Tracks pending and active participants
5. **Intelligent Fight Closure**: Based on participant viability and activity
6. **Event-Driven Architecture**: Real-time notifications for all fight events
7. **Robust Error Handling**: Handles edge cases and race conditions
8. **Integration Ready**: Plugs into existing game loop via coordination services

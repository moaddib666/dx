class GroupsNameResolver:
    delimiter = "::"
    label = ""

    def construct_group_name(self, *args):
        return self.delimiter.join([self.label, *[str(arg) for arg in args]])


class CharacterGroupsNameResolver(GroupsNameResolver):
    label = "character"

    def construct_character_online_group_name(self):
        return self.construct_group_name("online")

    def construct_character_online_id_group_name(self, character_id: str):
        return self.construct_group_name("online", character_id)


class CharacterActionGroupsNameResolver(GroupsNameResolver):
    label = "character_actions"

    def construct_character_action_group_name(self, character_id: str):
        return self.construct_group_name(character_id)


class FightGroupsNameResolver(GroupsNameResolver):
    label = "fight"

    def construct_fight_side_group_name(self, fight: str, side: str):
        return self.construct_group_name(fight, side)

    def construct_fight_group_name(self, fight: str):
        return self.construct_group_name(fight)

    def construct_participant_group_name(self, fight: str, participant: str):
        return self.construct_group_name(fight, "participant", participant)

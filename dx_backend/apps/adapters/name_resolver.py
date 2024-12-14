class GroupsNameResolver:
    delimiter = "::"
    label = ""

    def construct_group_name(self, *args):
        return self.delimiter.join([self.label, *[str(arg) for arg in args]])


class PlayerGroupsNameResolver(GroupsNameResolver):
    label = "player"

    def construct_player_online_group_name(self):
        return self.construct_group_name("online")

    def construct_player_online_id_group_name(self, player_id: str):
        return self.construct_group_name("online", player_id)


class PlayerActionGroupsNameResolver(GroupsNameResolver):
    label = "player_actions"

    def construct_player_action_group_name(self, player_id: str):
        return self.construct_group_name(player_id)


class FightGroupsNameResolver(GroupsNameResolver):
    label = "fight"

    def construct_fight_side_group_name(self, fight: str, side: str):
        return self.construct_group_name(fight, side)

    def construct_fight_group_name(self, fight: str):
        return self.construct_group_name(fight)

    def construct_participant_group_name(self, fight: str, participant: str):
        return self.construct_group_name(fight, "participant", participant)

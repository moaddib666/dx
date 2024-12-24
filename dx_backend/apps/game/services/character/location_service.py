from apps.character.models import Character
from apps.world.models import Location, City, SubLocation, Position


class LocationService:
    home_city_name = 'City of Memories'
    default_position = '00000000-0000-0000-0000-0193cb8bd8c4'

    def get_or_create_home(self, character: Character) -> Position:
        city = City.objects.get(name=self.home_city_name)
        home_location, created = Location.objects.get_or_create(
            name=character.name + "'s Home",
            defaults={
                'description': 'Default home location for new characters.',
                'is_active': True,
                'is_public': False,
            },
            area=city.area_set.first(),
            # TODO Add random area selection
        )
        room, _ = SubLocation.objects.get_or_create(
            name='Main Room',
            defaults={
                'description': 'Main room of the house.',
                'is_active': True,
            },
            location=home_location,
        )

        pos, _ = room.position_set.get_or_create(
            defaults={
                'x': character.id.int,
                'y': character.id.int,
                'z': -1000,
            },
        )

        return pos

    def default(self, character: Character, position: Position = None) -> Position:
        if not position:
            position = Position.objects.get(pk=self.default_position)
        return position

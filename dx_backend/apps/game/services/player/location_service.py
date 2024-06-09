from apps.player.models import Character
from apps.world.models import Location, City, SubLocation


class LocationService:
    home_city_name = 'City of Memories'

    def get_or_create_home_location(self, player: Character) -> Location:
        city = City.objects.get(name=self.home_city_name)
        home_location, created = Location.objects.get_or_create(
            name=player.name + "'s Home",
            defaults={
                'description': 'Default home location for new players.',
                'is_active': True,
                'is_public': False,
            },
            area=city.area_set.first(),
            # TODO Add random area selection
        )
        if not created:
            return home_location
        SubLocation.objects.get_or_create(
            name='Main Room',
            defaults={
                'description': 'Main room of the house.',
                'is_active': True,
            },
            location=home_location,
        )
        return home_location

from django.core.management.base import BaseCommand
from apps.character.models import Character, CharacterTemplate
from apps.game.services.npc.factory import NPCFactory, NPCFactoryConfig
from apps.skills.models import LearnedSchool
from apps.character.models.player import StatModifier
from apps.items.models import Item, WorldItem, CharacterItem
from apps.core.models import CharacterStats
from apps.client.models import Client
from apps.world.models import Position

class Command(BaseCommand):
    help = 'Test the fix for the IntegrityError in create_template_from_npc'

    def handle(self, *args, **options):
        # Create a factory
        factory = NPCFactory()

        # Find or create a client to use as the owner for our test character
        client = Client.objects.filter(is_staff=True).first()
        if not client:
            self.stdout.write(self.style.WARNING("No staff client found. Creating a test client."))
            client = Client.objects.create_user(
                email="test@example.com",
                password="testpassword",
                first_name="Test",
                last_name="User",
                is_staff=True
            )
            self.stdout.write(self.style.SUCCESS(f"Created test client: {client.email}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Using existing client: {client.email}"))

        # First, check if there's a template available
        template = CharacterTemplate.objects.first()
        if not template:
            # Create a template if none exists
            self.stdout.write(self.style.WARNING("No templates available. Creating a test template."))
            from apps.game.services.character.template import CharacterTemplateService
            template_service = CharacterTemplateService()
            template = template_service.create_template()
            template.name = "Test Template for Fix"
            template.save()
            self.stdout.write(self.style.SUCCESS(f"Created test template: {template.name}"))

        # Find an existing position
        position = Position.objects.first()
        if not position:
            self.stdout.write(self.style.ERROR("No positions available. Please create a position first."))
            return

        # Create a character directly instead of using the factory
        # This is because the factory doesn't support setting the owner
        npc = Character.objects.create(
            owner=client,
            name="Test NPC for Fix",
            organization=template.organization,
            tags=list(template.tags).copy() if template.tags else [],
            path=template.path,
            rank=template.rank,
            npc=True,
            behavior=template.behavior,
            dimension=template.dimension,
            position=position,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(f"Created NPC: {npc.name}"))

        # Add a school to the NPC
        try:
            from apps.school.models import School
            school = School.objects.first()
            if school:
                LearnedSchool.objects.create(
                    character=npc,
                    school=school,
                    is_base=True
                )
                self.stdout.write(self.style.SUCCESS(f"Added school: {school.name} to NPC"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Could not add school: {e}"))

        # Create a template from the NPC
        template_name = "Test Template from NPC Fix"
        new_template = factory.create_template_from_npc(npc, template_name)
        self.stdout.write(self.style.SUCCESS(f"Created template: {new_template.name}"))

        # Create a template from the NPC again (this would previously cause an IntegrityError)
        try:
            new_template2 = factory.create_template_from_npc(npc, template_name + " 2")
            self.stdout.write(self.style.SUCCESS(f"Created second template: {new_template2.name}"))

            # Create a template from the NPC a third time
            new_template3 = factory.create_template_from_npc(npc, template_name + " 3")
            self.stdout.write(self.style.SUCCESS(f"Created third template: {new_template3.name}"))

            self.stdout.write(self.style.SUCCESS("Test passed: No IntegrityError occurred when creating multiple templates from the same NPC"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Test failed: {e}"))

        # Clean up
        try:
            if 'new_template3' in locals():
                new_template3.delete()
            if 'new_template2' in locals():
                new_template2.delete()
            new_template.delete()
            npc.delete()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during cleanup: {e}"))

        self.stdout.write(self.style.SUCCESS("Test completed"))

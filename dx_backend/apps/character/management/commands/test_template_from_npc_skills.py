import time
from django.core.management.base import BaseCommand
from apps.character.models import Character, CharacterTemplate
from apps.game.services.npc.factory import NPCFactory, NPCFactoryConfig
from apps.skills.models import LearnedSkill
from apps.client.models import Client

class Command(BaseCommand):
    help = 'Test that skills are properly copied from an NPC to a template'

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

        # First, create an NPC from a template
        template = CharacterTemplate.objects.first()
        if not template:
            self.stdout.write(self.style.ERROR("No templates available. Please create a template first."))
            return

        # Create a character directly instead of using the factory
        # This is because the factory doesn't support setting the owner
        from apps.world.models import Position
        position = Position.objects.first()
        if not position:
            self.stdout.write(self.style.ERROR("No positions available. Please create a position first."))
            return

        npc = Character.objects.create(
            owner=client,
            name="Test NPC for Skills",
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

        # Add a skill to the NPC
        try:
            from apps.school.models import Skill
            skill = Skill.objects.first()
            if skill:
                LearnedSkill.objects.create(
                    character=npc,
                    skill=skill,
                    is_base=True
                )
                self.stdout.write(self.style.SUCCESS(f"Added skill: {skill.name} to NPC"))
            else:
                self.stdout.write(self.style.ERROR("No skills available. Please create a skill first."))
                npc.delete()
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Could not add skill: {e}"))
            npc.delete()
            return

        # Now create a template from the NPC
        timestamp = int(time.time())
        template_name = f"Test Template with Skills {timestamp}"
        new_template = factory.create_template_from_npc(npc, template_name)
        self.stdout.write(self.style.SUCCESS(f"Created template: {new_template.name}"))

        # Verify that the template has the expected skills
        skill_templates = new_template.skill_templates.all()
        self.stdout.write(self.style.SUCCESS(f"Template has {skill_templates.count()} skill templates"))
        for skill_template in skill_templates:
            self.stdout.write(self.style.SUCCESS(f"  - Skill: {skill_template.skill.name}, Is Base: {skill_template.is_base}"))

        # Finally, create a new NPC from the new template
        # Create a character directly instead of using the factory
        new_npc = Character.objects.create(
            owner=client,
            name="New Test NPC with Skills",
            organization=new_template.organization,
            tags=list(new_template.tags).copy() if new_template.tags else [],
            path=new_template.path,
            rank=new_template.rank,
            npc=True,
            behavior=new_template.behavior,
            dimension=new_template.dimension,
            position=position,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(f"Created new NPC from template: {new_npc.name}"))

        # Apply template skills manually
        for skill_template in new_template.skill_templates.all():
            LearnedSkill.objects.create(
                character=new_npc,
                skill=skill_template.skill,
                is_base=skill_template.is_base
            )

        # Verify that the new NPC has the expected skills
        learned_skills = new_npc.learned_skills.all()
        self.stdout.write(self.style.SUCCESS(f"New NPC has {learned_skills.count()} learned skills"))
        for learned_skill in learned_skills:
            self.stdout.write(self.style.SUCCESS(f"  - Skill: {learned_skill.skill.name}, Is Base: {learned_skill.is_base}"))

        # Clean up
        new_npc.delete()
        new_template.delete()
        npc.delete()

        self.stdout.write(self.style.SUCCESS("Test completed successfully!"))

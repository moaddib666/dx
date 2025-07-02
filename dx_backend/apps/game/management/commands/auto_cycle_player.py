import time
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.action.models import Cycle
from apps.game.models import Campaign
from apps.gamemaster.tools import ACTION_PIPELINE_TOOL


class Command(BaseCommand):
    help = 'Auto cycle player for campaigns with auto_play=True. Runs every 1.30 minutes.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting auto cycle player...'))
        self.loop()

    def process_auto_play_campaigns(self):
        # Find all campaigns with auto_play=True
        auto_play_campaigns = Campaign.objects.filter(auto_play=True, is_active=True)

        if not auto_play_campaigns.exists():
            self.stdout.write(self.style.WARNING('No auto-play campaigns found.'))
            return

        for campaign in auto_play_campaigns:
            self.stdout.write(f"Processing campaign: {campaign.name}")

            try:
                # Get the current cycle for the campaign
                current_cycle = Cycle.objects.current(campaign=campaign)

                # Create a cycle player service
                svc = ACTION_PIPELINE_TOOL.cycle_player_factory(
                    cycle=current_cycle,
                    factory=ACTION_PIPELINE_TOOL.action_factory
                )

                # Play the cycle
                new_cycle = svc.play()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully advanced campaign '{campaign.name}' to cycle {new_cycle.number}"
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error processing campaign '{campaign.name}': {str(e)}"
                    )
                )

    def loop(self):
        interval_seconds = 90  # 1.30 minutes = 90 seconds

        while True:
            start_time = timezone.now()
            self.stdout.write(f"Running cycle at {start_time}")

            try:
                self.process_auto_play_campaigns()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error in auto cycle player: {str(e)}"))

            # Calculate how long to sleep
            elapsed = (timezone.now() - start_time).total_seconds()
            sleep_time = max(0, interval_seconds - elapsed)

            if sleep_time > 0:
                self.stdout.write(f"Sleeping for {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)

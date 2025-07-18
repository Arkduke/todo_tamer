from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task

class Command(BaseCommand):
    help = 'Update task statuses based on current time'
    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output',
        )
    
    def handle(self, *args, **options):
        verbose = options['verbose']
        
        tasks = Task.objects.all()
        updated_count = 0
        
        for task in tasks:
            old_status = task.status
            new_status = task.get_auto_status()
            
            if old_status != new_status:
                task.status = new_status
                task.save(update_fields=['status'])
                updated_count += 1
                
                if verbose:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Updated task "{task.title}" from {old_status} to {new_status}'
                        )
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} tasks out of {tasks.count()} total tasks'
            )
        )
        
        if verbose:
            upcoming = Task.objects.filter(status='upcoming').count()
            completed = Task.objects.filter(status='completed').count()
            missed = Task.objects.filter(status='missed').count()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Current status: {upcoming} upcoming, {completed} completed, {missed} missed'
                )
            )

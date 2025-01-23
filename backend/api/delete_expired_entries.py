from django.core.management.base import BaseCommand
from django.utils.timezone import now
from api.models import BlocklistItem

class Command(BaseCommand):
    help = 'Deletes blocklist entries with auto_delete set to True and delete_date set to today or earlier'

    def handle(self, *args, **kwargs):
        today = now().date()
        expired_entries = BlocklistItem.objects.filter(auto_delete=True, delete_date__lte=today)
        count = expired_entries.count()
        expired_entries.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired blocklist entries'))


#Add to contrab editor
#crontab -e
#0 0 * * * /path/to/your/virtualenv/bin/python /path/to/your/project/manage.py delete_expired_entries
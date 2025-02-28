from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
import os
import pytz
from datetime import datetime
from django.utils.timezone import now

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title


class BlocklistItem(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('IP', 'IP Address'),
        ('DOMAIN', 'Domain'),
    ]

    entry = models.CharField(max_length=255, unique=True)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES, default='IP')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.entry

    def save(self, *args, **kwargs):
        if not self.is_valid_entry(self.entry):
            raise ValidationError(f"{self.entry} is not a valid IP address or domain")
        self.entry_type = self.get_entry_type(self.entry)
        super().save(*args, **kwargs)
        self.update_blocklist_files()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_blocklist_files()

    @staticmethod
    def is_valid_entry(entry):
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        domain_pattern = re.compile(r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.\w+)?$')
        return ip_pattern.match(entry) is not None or domain_pattern.match(entry) is not None

    @staticmethod
    def get_entry_type(entry):
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        if ip_pattern.match(entry):
            return 'IP'
        else:
            return 'DOMAIN'

    @staticmethod
    def update_blocklist_files():
        blocklist_items = BlocklistItem.objects.all()
        master_file_path = os.path.join(os.path.dirname(__file__), '../../index/edl/master_blocklist/master_blocklist.txt')
        ip_file_path = os.path.join(os.path.dirname(__file__), '../../index/edl/ip/blocklist.txt')
        domain_file_path = os.path.join(os.path.dirname(__file__), '../../index/edl/domain/blocklist.txt')
        cst = pytz.timezone('America/Chicago')

        try:
            with open(master_file_path, 'w') as master_file, \
                 open(ip_file_path, 'w') as ip_file, \
                 open(domain_file_path, 'w') as domain_file:
                
                # Write "type=string" at the top of the domain blocklist file
                domain_file.write('type=string\n')
                
                for item in blocklist_items:
                    added_by = item.added_by.username if item.added_by else "None"
                    added_on_cst = item.added_on.astimezone(cst).strftime('%Y-%m-%d %H:%M:%S %Z')
                    entry_line = f'"{item.entry}" "{added_on_cst}" "{added_by}" "{item.notes}"\n'
                    
                    master_file.write(entry_line)
                    
                    if item.entry_type == 'IP':
                        ip_file.write(f'{item.entry}\n')
                    elif item.entry_type == 'DOMAIN':
                        domain_file.write(f'{item.entry}\n')
            
            print(f"Blocklist files successfully created at {master_file_path}, {ip_file_path}, and {domain_file_path}")
        except Exception as e:
            print(f"Error creating blocklist files: {e}")

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
import os
import pytz
from datetime import datetime

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title


class BlocklistItem(models.Model):
    entry = models.CharField(max_length=255, unique=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    auto_delete = models.BooleanField(default=False)
    delete_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.entry

    def save(self, *args, **kwargs):
        if not self.is_valid_entry(self.entry):
            raise ValidationError(f"{self.entry} is not a valid IP address or domain")
        super().save(*args, **kwargs)
        self.update_master_blocklist()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_master_blocklist()

    @staticmethod
    def is_valid_entry(entry):
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\.\w+)?$')
        domain_pattern = re.compile(
            r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.\w+)?$'
        )
        return ip_pattern.match(entry) or domain_pattern.match(entry)

    @staticmethod
    def update_master_blocklist():
        blocklist_items = BlocklistItem.objects.all()
        file_path = os.path.join(os.path.dirname(__file__), '../../index/edl/master_blocklist/master_blocklist.txt')
        cst = pytz.timezone('America/Chicago')
        try:
            with open(file_path, 'w') as file:
                for item in blocklist_items:
                    added_by = item.added_by.username if item.added_by else "None"
                    added_on_cst = item.added_on.astimezone(cst).strftime('%Y-%m-%d %H:%M:%S %Z')
                    delete_date_str = item.delete_date.strftime('%Y-%m-%d') if item.delete_date else "None"
                    file.write(f'"{item.entry}" "{added_on_cst}" "auto_delete: {item.auto_delete}" '
                               f'"{delete_date_str}" "{added_by}" "{item.notes}"\n')
            print(f"master_blocklist.txt successfully updated at {file_path}")
        except Exception as e:
            print(f"Error creating master_blocklist.txt: {e}")


        
class IPList(models.Model):
    ip = models.CharField(max_length=255, unique=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip

    def save(self, *args, **kwargs):
        if not self.is_valid_ip(self.ip):
            raise ValidationError(f"{self.ip} is not a valid IP address")
        super().save(*args, **kwargs)

    @staticmethod
    def is_valid_ip(ip):
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        return ip_pattern.match(ip) is not None
    
class DomainList(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.domain

    def save(self, *args, **kwargs):
        if not self.is_valid_domain_or_ip(self.domain):
            raise ValidationError(f"{self.domain} is not a valid domain or IP address")
        super().save(*args, **kwargs)

    @staticmethod
    def is_valid_domain_or_ip(entry):
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\.\w+)?$')
        domain_pattern = re.compile(
            r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.\w+)?$'
        )
        return ip_pattern.match(entry) or domain_pattern.match(entry)

    def __str__(self):
        return self.domain
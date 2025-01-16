from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title


class BlocklistItem(models.Model):
    entry = models.CharField(max_length=255, unique=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # Fixed on_delete
    added_on = models.DateTimeField(auto_now_add=True)
    auto_delete = models.BooleanField(default=False)
    delete_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.entry

    def save(self, *args, **kwargs):
        # if not self.added_by:
        #     raise ValidationError("Created by field cannot be empty")
        if not self.is_valid_entry(self.entry):
            raise ValidationError(f"{self.entry} is not a valid IP address or domain")
        super().save(*args, **kwargs)

    @staticmethod
    def is_valid_entry(entry):
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\.\w+)?$')
        domain_pattern = re.compile(
            r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.\w+)?$'
        )
        return ip_pattern.match(entry) or domain_pattern.match(entry)

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
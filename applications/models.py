from django.db import models
from django.utils import timezone
import uuid

class Application(models.Model):
    class Status(models.TextChoices):
        SUBMITTED="SUBMITTED","Submitted"
        APPROVED="APPROVED","Approved"
        VM_ASSIGNED="VM_ASSIGNED","VM Assigned"
        CLOSED="CLOSED","Closed"

    first_name  = models.CharField(max_length=80)
    last_name   = models.CharField(max_length=80)
    email       = models.EmailField()
    course      = models.CharField(max_length=120, blank=True)
    reason      = models.TextField(blank=True)

    status      = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    vm_id       = models.CharField(max_length=120, blank=True)
    staff_notes = models.TextField(blank=True)

    status_token= models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.email})"

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['deadline']),
            models.Index(fields=['status']),
            models.Index(fields=['is_completed']),
        ]
        
    def __str__(self):
        return self.title
    
    def clean(self):
        if not self.pk and self.deadline <= timezone.now():
            raise ValidationError("Deadline cannot be in the past.")
        
    def save(self,*args,**kwargs):
        if self.is_completed:
            self.status = 'completed'
            if not self.completed_at:
                self.completed_at = timezone.now()
        else:
            self.completed_at = None
            self.status=self.get_auto_status()
        super().save(*args,**kwargs)
            
    def get_auto_status(self):
        if self.is_completed:
            return 'completed'
        elif self.deadline <= timezone.now():
            return 'missed'
        else:
            return 'upcoming'
        
    def mark_completed(self):
        self.is_completed=True
        self.save()
        
    def mark_incomplete(self):
        self.is_completed = False
        self.save()
    
    @property
    def is_overdue(self):
        return not self.is_completed and self.deadline <= timezone.now()
    
    @property
    def time_until_deadline(self):
        if self.deadline <= timezone.now():
            return None
        return self.deadline - timezone.now()
    
    @property
    def urgency_level(self):
        if self.is_completed:
            return 'completed'
        
        if self.deadline <= timezone.now():
            return 'missed'
        
        time_left = self.time_until_deadline
        if time_left.days <= 1:
            return 'high'
        elif time_left.days <= 3:
            return 'medium'
        else:
            return 'low'

from rest_framework import serializers
from django.utils import timezone
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    urgency_level = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    time_until_deadline = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'deadline', 'status',
            'is_completed', 'created_at', 'updated_at', 'completed_at',
            'urgency_level', 'is_overdue', 'time_until_deadline'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at', 'completed_at']
    
    def validate_deadline(self, value):
        if not self.instance and value <= timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value
    
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'is_completed']
    
    def validate_deadline(self, value):
        if self.instance and self.instance.is_completed:
            raise serializers.ValidationError("Cannot update deadline of completed task.")
        return value


class TaskStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['is_completed']


class TaskBucketSerializer(serializers.Serializer):
    upcoming = TaskSerializer(many=True, read_only=True)
    completed = TaskSerializer(many=True, read_only=True)
    missed = TaskSerializer(many=True, read_only=True)
    
    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance
        
        upcoming_tasks = []
        completed_tasks = []
        missed_tasks = []
        
        for task in instance:
            task.status = task.get_auto_status()
            task.save(update_fields=['status'])
            
            if task.status == 'upcoming':
                upcoming_tasks.append(task)
            elif task.status == 'completed':
                completed_tasks.append(task)
            elif task.status == 'missed':
                missed_tasks.append(task)
        
        return {
            'upcoming': TaskSerializer(upcoming_tasks, many=True).data,
            'completed': TaskSerializer(completed_tasks, many=True).data,
            'missed': TaskSerializer(missed_tasks, many=True).data,
        }

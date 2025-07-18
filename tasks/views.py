from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from datetime import timedelta
import json
from .models import Task
from .serializer import (
    TaskSerializer, 
    TaskUpdateSerializer, 
    TaskStatusSerializer,
    TaskBucketSerializer
)
from .ai_service import AIService


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return TaskUpdateSerializer
        elif self.action in ['mark_completed', 'mark_incomplete']:
            return TaskStatusSerializer
        return TaskSerializer
    
    def get_queryset(self):
        queryset = Task.objects.all()
        
        for task in queryset:
            old_status = task.status
            new_status = task.get_auto_status()
            if old_status != new_status:
                task.status = new_status
                task.save(update_fields=['status'])
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        urgency_filter = self.request.query_params.get('urgency')
        if urgency_filter:
            now = timezone.now()
            if urgency_filter == 'high':
                queryset = queryset.filter(
                    deadline__lte=now + timezone.timedelta(days=1),
                    is_completed=False
                )
            elif urgency_filter == 'medium':
                queryset = queryset.filter(
                    deadline__lte=now + timezone.timedelta(days=3),
                    deadline__gt=now + timezone.timedelta(days=1),
                    is_completed=False
                )
            elif urgency_filter == 'low':
                queryset = queryset.filter(
                    deadline__gt=now + timezone.timedelta(days=3),
                    is_completed=False
                )
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        task = serializer.save()
        task.status = task.get_auto_status()
        task.save(update_fields=['status'])
    
    def perform_update(self, serializer):
        task = serializer.save()
        task.status = task.get_auto_status()
        task.save(update_fields=['status'])
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        task = self.get_object()
        task.mark_completed()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_incomplete(self, request, pk=None):
        task = self.get_object()
        task.mark_incomplete()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def buckets(self, request):
        queryset = self.get_queryset()
        
        for task in queryset:
            task.status = task.get_auto_status()
            task.save(update_fields=['status'])
        
        upcoming_tasks = queryset.filter(status='upcoming')
        completed_tasks = queryset.filter(status='completed')
        missed_tasks = queryset.filter(status='missed')
        
        data = {
            'upcoming': TaskSerializer(upcoming_tasks, many=True).data,
            'completed': TaskSerializer(completed_tasks, many=True).data,
            'missed': TaskSerializer(missed_tasks, many=True).data,
        }
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'upcoming': queryset.filter(status='upcoming').count(),
            'completed': queryset.filter(status='completed').count(),
            'missed': queryset.filter(status='missed').count(),
            'high_urgency': queryset.filter(
                deadline__lte=timezone.now() + timezone.timedelta(days=1),
                is_completed=False
            ).count(),
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['post'])
    def ai_create(self, request):
        natural_language = request.data.get('natural_language', '')
        
        if not natural_language:
            return Response(
                {"error": "Natural language input is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ai_service = AIService()
        try:
            ai_analysis = ai_service.create_task_from_natural_language(natural_language)
            return Response(ai_analysis)
        except Exception as e:
            return Response(
                {"error": f"AI processing failed: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def ai_breakdown(self, request, pk=None):
        task = self.get_object()
        
        ai_service = AIService()
        try:
            breakdown = ai_service.break_down_task(task.title, task.description)
            return Response(breakdown)
        except Exception as e:
            return Response(
                {"error": f"AI breakdown failed: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def ai_enhance(self, request, pk=None):
        task = self.get_object()
        
        ai_service = AIService()
        try:
            enhancement = ai_service.enhance_task_description(task.title, task.description)
            return Response(enhancement)
        except Exception as e:
            return Response(
                {"error": f"AI enhancement failed: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def ai_insights(self, request):
        queryset = self.get_queryset()
        total_tasks = queryset.count()
        
        if total_tasks == 0:
            return Response({
                "assessment": "No tasks available for analysis",
                "recommendations": ["Start by creating some tasks!"],
                "patterns": ["Need more data for analysis"],
                "motivational_message": "Begin your productivity journey!"
            })
        
        completed_tasks = queryset.filter(status='completed').count()
        missed_tasks = queryset.filter(status='missed').count()
        high_urgency_tasks = queryset.filter(
            deadline__lte=timezone.now() + timedelta(days=1),
            is_completed=False
        ).count()
        
        completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        task_stats = {
            'total': total_tasks,
            'completed': completed_tasks,
            'missed': missed_tasks,
            'high_urgency': high_urgency_tasks,
            'completion_rate': completion_rate
        }
        
        ai_service = AIService()
        try:
            insights = ai_service.generate_productivity_insights(task_stats)
            return Response(insights)
        except Exception as e:
            return Response(
                {"error": f"AI insights failed: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def ai_conflicts(self, request):
        queryset = self.get_queryset().filter(status='upcoming')
        
        tasks_data = []
        for task in queryset:
            tasks_data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'deadline': task.deadline.isoformat(),
                'urgency': task.urgency_level
            })
        
        ai_service = AIService()
        try:
            conflicts = ai_service.detect_task_conflicts(tasks_data)
            return Response(conflicts)
        except Exception as e:
            return Response(
                {"error": f"AI conflict detection failed: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def ai_reminder(self, request, pk=None):
        task = self.get_object()
        
        ai_service = AIService()
        try:
            reminder = ai_service.generate_smart_reminder(
                task.title, 
                task.description, 
                task.deadline
            )
            return Response({"reminder": reminder})
        except Exception as e:
            return Response(
                {"error": f"AI reminder failed: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

def home_view(request):
    return render(request, 'home.html')
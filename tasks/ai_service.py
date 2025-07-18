import json
import openai
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(__name__)

class AIService:    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def create_task_from_natural_language(self, natural_language_input):
        prompt = f"""
        Analyze this task request and extract structured information:
        
        Request: "{natural_language_input}"
        
        Extract:
        1. A clear, concise task title (max 100 chars)
        2. A detailed description explaining what needs to be done
        3. A suggested deadline (ISO format, relative to today: {timezone.now().date()})
        4. If only day is mentioned (like by monday or saturday) in the timeline select a date in the future that is greater than {timezone.now().date()}).
        5. Priority level (high/medium/low)
        6. Estimated duration in hours
        7. 3-5 actionable subtasks
        8. Category/tags that would help organize this task
                
        Respond ONLY with valid JSON in this exact format:
        {{
            "title": "Clear task title",
            "description": "Detailed description of what needs to be done",
            "suggested_deadline": "2025-07-20T15:00:00",
            "priority": "medium",
            "estimated_duration": 3.5,
            "subtasks": ["Subtask 1", "Subtask 2", "Subtask 3"],
            "category": "Work",
            "tags": ["meeting", "presentation", "client"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error in AI task creation: {str(e)}")
            return {
                "error": f"AI processing failed: {str(e)}",
                "title": "AI Task Creation Failed",
                "description": f"Original request: {natural_language_input}",
                "suggested_deadline": (timezone.now() + timedelta(days=1)).isoformat(),
                "priority": "medium",
                "estimated_duration": 1.0,
                "subtasks": ["Review original request", "Create task manually"],
                "category": "General",
                "tags": ["ai-failed"]
            }
    
    def break_down_task(self, task_title, task_description):
        prompt = f"""
        Break down this task into 3-6 specific, actionable subtasks:
        
        Title: {task_title}
        Description: {task_description}
        
        Each subtask should be:
        - Specific and actionable
        - Achievable in 1-4 hours
        - Clearly defined with measurable outcomes
        
        Respond ONLY with valid JSON:
        {{
            "subtasks": [
                "Specific subtask 1",
                "Specific subtask 2",
                "Specific subtask 3"
            ],
            "estimated_total_hours": 8.5,
            "suggested_order": [
                "Brief explanation of why this order is recommended"
            ]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error in AI task breakdown: {str(e)}")
            return {
                "subtasks": ["Review task requirements", "Plan approach", "Execute task"],
                "estimated_total_hours": 4.0,
                "suggested_order": ["Standard breakdown due to AI processing error"]
            }
    
    def enhance_task_description(self, task_title, current_description=""):
        prompt = f"""
        Enhance this task description to make it more actionable and clear:
        
        Title: {task_title}
        Current Description: {current_description if current_description else "No description provided"}
        
        Provide:
        1. An enhanced description that's clear and actionable
        2. Success criteria (how to know when it's done)
        3. Potential challenges and solutions
        4. Required resources or tools
        
        Respond ONLY with valid JSON:
        {{
            "enhanced_description": "Clear, actionable description",
            "success_criteria": ["Criterion 1", "Criterion 2"],
            "potential_challenges": ["Challenge 1", "Challenge 2"],
            "required_resources": ["Resource 1", "Resource 2"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error in AI task enhancement: {str(e)}")
            return {
                "enhanced_description": f"Enhanced task: {task_title}. {current_description}",
                "success_criteria": ["Task completed successfully"],
                "potential_challenges": ["Time management", "Resource availability"],
                "required_resources": ["Time", "Focus"]
            }
    
    def generate_productivity_insights(self, task_stats):
        prompt = f"""
        Analyze these productivity metrics and provide actionable insights:
        
        Statistics:
        - Total tasks: {task_stats.get('total', 0)}
        - Completed tasks: {task_stats.get('completed', 0)}
        - Missed tasks: {task_stats.get('missed', 0)}
        - High urgency tasks: {task_stats.get('high_urgency', 0)}
        - Completion rate: {task_stats.get('completion_rate', 0)}%
        
        Provide:
        1. Overall productivity assessment
        2. 3 specific actionable recommendations
        3. Patterns or trends you notice
        4. Motivational message
        
        Respond ONLY with valid JSON:
        {{
            "assessment": "Overall productivity assessment",
            "recommendations": ["Recommendation 1", "Recommendation 2", "Recommendation 3"],
            "patterns": ["Pattern 1", "Pattern 2"],
            "motivational_message": "Encouraging message"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.4
            )
            
            content = response.choices[0].message.content.strip()
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error in AI productivity insights: {str(e)}")
            return {
                "assessment": "Unable to generate detailed assessment due to AI processing error",
                "recommendations": ["Review task management approach", "Set realistic deadlines", "Focus on high-priority tasks"],
                "patterns": ["Need more data for pattern analysis"],
                "motivational_message": "Keep working towards your goals!"
            }
    
    def detect_task_conflicts(self, tasks_data):
        prompt = f"""
        Analyze these tasks for potential conflicts and scheduling issues:
        
        Tasks: {json.dumps(tasks_data, indent=2)}
        
        Look for:
        1. Overlapping deadlines that might cause stress
        2. Tasks that should be done in sequence
        3. Unrealistic time expectations
        4. Resource conflicts
        
        Respond ONLY with valid JSON:
        {{
            "conflicts": [
                {{
                    "type": "deadline_overlap",
                    "description": "Description of conflict",
                    "affected_tasks": ["Task 1", "Task 2"],
                    "suggestion": "How to resolve"
                }}
            ],
            "recommendations": ["Overall recommendation 1", "Overall recommendation 2"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=700,
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error in AI conflict detection: {str(e)}")
            return {
                "conflicts": [],
                "recommendations": ["Review task scheduling", "Ensure realistic deadlines"]
            }
    
    def generate_smart_reminder(self, task_title, task_description, deadline):
        time_until_deadline = deadline - timezone.now()
        days_left = time_until_deadline.days
        
        prompt = f"""
        Generate a motivational and personalized reminder for this task:
        
        Task: {task_title}
        Description: {task_description}
        Days until deadline: {days_left}
        
        Make it:
        - Motivational and encouraging
        - Specific to the task
        - Appropriate for the urgency level
        - Personal and engaging
        
        Respond with just the reminder message, no JSON formatting needed.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.6
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error in AI reminder generation: {str(e)}")
            return f"Reminder: Don't forget about '{task_title}' - {days_left} days remaining!"

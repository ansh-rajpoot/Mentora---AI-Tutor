from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 1. Level System
class Level(models.Model):
    number = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    xp_threshold = models.IntegerField(help_text="Total XP required to reach this level")

    def __str__(self):
        return f"Level {self.number}: {self.title} ({self.xp_threshold} XP)"

# 2. User Profile
class UserProfile(models.Model):
    PLAN_CHOICES = [
        ('FREE', 'Free Student'),
        ('BASIC', 'Pro Student'),
        ('ULTRA', 'Ultra Explorer'),
    ]
    
    SKILL_LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True, help_text="Tell us about yourself")
    interests = models.TextField(blank=True, help_text="What do you love learning about?")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='BEGINNER')
    
    # Gamification fields
    total_xp = models.IntegerField(default=0)
    current_level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    current_streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)
    quizzes_completed = models.IntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)
    
    # Settings
    is_2fa_enabled = models.BooleanField(default=False)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='FREE')
    questions_asked = models.IntegerField(default=0)

    def __str__(self):
        lvl_num = self.current_level.number if self.current_level else 1
        return f"{self.user.username}'s Profile - Level {lvl_num}"

# 3. Quiz System
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, default='book')

    def __str__(self):
        return self.name

class Quiz(models.Model):
    DIFFICULTY_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='BEGINNER')
    xp_reward = models.IntegerField(default=50)
    time_limit_seconds = models.IntegerField(default=300)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"{self.subject.name} - {self.title}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Q: {self.text[:50]}..."

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField()
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_taken_seconds = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}/{self.total_questions})"

class UserAnswer(models.Model):
    attempt = models.ForeignKey(UserQuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

# 4. Achievements
class Achievement(models.Model):
    TYPE_CHOICES = [
        ('XP', 'XP Milestone'),
        ('STREAK', 'Streak Milestone'),
        ('QUIZ_COUNT', 'Quizzes Completed'),
        ('SUBJECT_MASTER', 'Subject Master'),
    ]
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Lucide icon name")
    description = models.TextField()
    xp_required = models.IntegerField(default=0)
    streak_required = models.IntegerField(default=0)
    quiz_count_required = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

# 5. Engagement & History
class XPTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xp_history')
    amount = models.IntegerField()
    reason = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} +{self.amount} XP ({self.reason})"

class WeeklyLeaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start = models.DateField()
    xp_gained = models.IntegerField(default=0)
    rank = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'week_start')

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    topic = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.topic}"

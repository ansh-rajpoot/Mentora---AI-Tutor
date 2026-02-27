from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Level, Achievement, UserAchievement, XPTransaction, Quiz, UserQuizAttempt

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['number', 'title', 'xp_threshold']

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['name', 'description', 'icon', 'xp_required', 'streak_required', 'quiz_count_required']

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)
    class Meta:
        model = UserAchievement
        fields = ['achievement', 'unlocked_at']

class XPTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = XPTransaction
        fields = ['amount', 'reason', 'timestamp']

class DashboardStatsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    full_name = serializers.CharField()
    level = serializers.SerializerMethodField()
    achievements_count = serializers.SerializerMethodField()
    recent_achievements = serializers.SerializerMethodField()
    quizzes_remaining = serializers.SerializerMethodField()
    xp_to_next_level = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'username', 'full_name', 'total_xp', 'level', 'current_streak', 'max_streak', 
            'achievements_count', 'recent_achievements', 'quizzes_remaining', 
            'xp_to_next_level', 'progress_percentage'
        ]

    def get_level(self, obj):
        if obj.current_level:
            return LevelSerializer(obj.current_level).data
        return {"number": 1, "title": "Smart Explorer", "xp_threshold": 100}

    def get_achievements_count(self, obj):
        return obj.user.achievements.count()

    def get_recent_achievements(self, obj):
        achs = obj.user.achievements.all().order_by('-unlocked_at')[:4]
        return UserAchievementSerializer(achs, many=True).data

    def get_quizzes_remaining(self, obj):
        total_quizzes = Quiz.objects.count()
        completed = UserQuizAttempt.objects.filter(user=obj.user).values('quiz').distinct().count()
        return max(0, total_quizzes - completed)

    def get_xp_to_next_level(self, obj):
        # 100 XP per level increment
        xp_in_level = obj.total_xp % 100
        return 100 - xp_in_level

    def get_progress_percentage(self, obj):
        return obj.total_xp % 100

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from .models import XPTransaction, UserProfile, Level, Achievement, UserAchievement, LoginHistory
from .services import award_xp, check_achievements

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ Automatically create a UserProfile when a new User is registered. """
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(user_logged_in)
def track_login(sender, request, user, **kwargs):
    """ Record login activity and award daily login XP """
    ip = request.META.get('REMOTE_ADDR')
    ua = request.META.get('HTTP_USER_AGENT')
    LoginHistory.objects.create(user=user, ip_address=ip, user_agent=ua)
    
    # Award daily login XP (+10)
    award_xp(user, 10, "Daily Login Reward")

@receiver(post_save, sender=XPTransaction)
def handle_xp_transaction(sender, instance, created, **kwargs):
    """
    NOTE: XP is now primarily handled in services.award_xp.
    This signal remains as a fallback or for direct model manipulation tracking.
    """
    if created:
        # We check achievements again just in case XP was added via direct model creation
        check_achievements(instance.user)

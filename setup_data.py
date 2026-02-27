import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_teacher_backend.settings')
django.setup()

from core.models import Level, Achievement, Subject

def run():
    print("Initializing Mentora Data...")

    # 1. Levels
    levels = [
        (1, "Smart Explorer", 0),
        (2, "Curious Mind", 100),
        (3, "Knowledge Seeker", 200),
        (4, "Logic Master", 300),
        (5, "Bright Scholar", 400),
        (6, "Insight Wizard", 500),
        (7, "Wisdom Keeper", 600),
        (8, "Genius Apprentice", 700),
        (9, "Cognitive Titan", 800),
        (10, "AI Mastermind", 900),
    ]
    for num, title, xp in levels:
        Level.objects.get_or_create(number=num, defaults={'title': title, 'xp_threshold': xp})
    print(f"Created {len(levels)} levels.")

    # 2. Achievements
    achs = [
        ("The Beginning", "rocket", "Start your learning journey", 0, 0, 0),
        ("XP Collector", "coins", "Earn 100 XP", 100, 0, 0),
        ("Streak Starter", "flame", "Maintain a 3-day streak", 0, 3, 0),
        ("Quiz Master", "award", "Complete 5 quizzes", 0, 0, 5),
        ("Knowledge Hub", "brain", "Earn 500 XP", 500, 0, 0),
        ("Undefeated", "trophy", "Maintain a 7-day streak", 0, 7, 0),
    ]
    for name, icon, desc, xp, streak, quiz in achs:
        Achievement.objects.get_or_create(
            name=name,
            defaults={
                'icon': icon,
                'description': desc,
                'xp_required': xp,
                'streak_required': streak,
                'quiz_count_required': quiz
            }
        )
    print(f"Created {len(achs)} achievements.")

    # 3. Subjects
    subjects = ["History", "Astronomy", "Science", "Philosophy", "Art", "Math"]
    for s_name in subjects:
        Subject.objects.get_or_create(name=s_name)
    print(f"Created {len(subjects)} subjects.")

    print("Setup Complete!")

if __name__ == "__main__":
    run()

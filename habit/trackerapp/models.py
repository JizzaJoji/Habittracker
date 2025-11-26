from django.db import models
from django.utils import timezone
from datetime import timedelta, date
from collections import Counter

class Habit(models.Model):
    CATEGORY_CHOICES = [
        ('health', 'Health'),
        ('work', 'Work'),
        ('learning', 'Learning'),
        ('personal', 'Personal Development'),
    ]

    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

    def total_checkins(self):
        return self.checkin_set.count()

    def success_rate(self):
        total_days = (timezone.now().date() - self.start_date).days + 1
        if total_days == 0:
            return 0
        return round((self.checkin_set.count() / total_days) * 100, 2)

    def best_day(self):
        checkins = self.checkin_set.all()
        if not checkins:
            return None
        day_counts = Counter([c.date.weekday() for c in checkins])
        best_day_index = day_counts.most_common(1)[0][0]
        # Map index to readable day name
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return days[best_day_index]

    def weekly_summary(self):
        summary = {}
        checkins = self.checkin_set.all()
        for c in checkins:
            # ISO calendar: year, week number
            year, week, _ = c.date.isocalendar()
            key = f"{year}-W{week}"
            summary[key] = summary.get(key, 0) + 1
        return summary

    def streak(self):
        checkins = self.checkin_set.order_by('-date')
        if not checkins:
            return 0

        streak = 0
        today = timezone.now().date()
        for c in checkins:
            if c.date == today - timedelta(days=streak):
                streak += 1
            else:
                break
        return streak


class CheckIn(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ('habit', 'date')  # prevent multiple check-ins per day

    def __str__(self):
        return f"{self.habit.name} - {self.date}"

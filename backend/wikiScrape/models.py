from django.db import models
from django.contrib.auth.models import User

#Create WikiScrape Model
class WikiScrape(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scrapes')

    url = models.URLField()
    title = models.CharField(max_length=255)
    summary = models.TextField()
    sections = models.JSONField(default=list)
    key_entities = models.JSONField(default=dict)
    related_topics = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#Create Quiz Model
class Quiz(models.Model):

    class Difficulty(models.TextChoices):
        EASY = 'easy', 'Easy'
        MEDIUM = 'medium', 'Medium'
        HARD = 'hard', 'Hard'

    scrape = models.ForeignKey(WikiScrape, on_delete=models.CASCADE, related_name='quizzes')

    question = models.TextField()
    options = models.JSONField(default=list)
    answer = models.CharField(max_length=255)
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.EASY
    )
    explanation = models.TextField()

    def __str__(self):
        return f"Quiz for {self.scrape.title}"

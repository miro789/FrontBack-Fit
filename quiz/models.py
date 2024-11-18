from django.db import models

class Question(models.Model):
    topic = models.CharField(max_length=255)
    scenario = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    choice_a = models.TextField()
    choice_a_type = models.CharField(max_length=20, choices=[('frontend', 'Frontend'), ('backend', 'Backend')])
    choice_b = models.TextField()
    choice_b_type = models.CharField(max_length=20, choices=[('frontend', 'Frontend'), ('backend', 'Backend')])

    def __str__(self):
        return self.topic

class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=255)  # Unique ID for tracking user sessions
    answer = models.CharField(max_length=1, choices=[('A', 'Choice A'), ('B', 'Choice B')])

class AppRating(models.Model):
    user_id = models.CharField(max_length=255)
    rating = models.IntegerField()  # 1 to 5 stars


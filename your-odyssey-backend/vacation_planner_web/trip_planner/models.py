from django.db import models


class TripPlan(models.Model):
    destination = models.CharField(max_length=100)
    days = models.IntegerField()
    budget_level = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.destination} - {self.days} days"


class UserQuery(models.Model):
    query_text = models.TextField()
    response_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query: {self.query_text[:50]}..."
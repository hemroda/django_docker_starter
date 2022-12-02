from django.db import models


class Post(models.Model):
    author = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author}"

from django.db import models

class CompanyInfo(models.Model):
    topic = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.topic

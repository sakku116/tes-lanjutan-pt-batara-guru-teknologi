from django.db import models
from django.conf import settings

# Create your models here.
class Url(models.Model):
    long_url = models.CharField(max_length=2048)
    short_url = models.CharField(max_length=2048)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 

    def as_dict(self):
        return {
            "id": self.id,
            "long_url": self.long_url,
            "short_url": self.short_url,
            "owner": self.owner
        }
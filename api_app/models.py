from django.db import models
from django.conf import settings

# Create your models here.
class Url(models.Model):
    long_url = models.CharField(max_length=2048, default="")
    short_url = models.CharField(max_length=2048, default="")
    owner_id = models.IntegerField(null=True, default=0) 
    created_at = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {
            "id": self.id,
            "long_url": self.long_url,
            "short_url": self.short_url,
            "created_at": self.created_at
        }
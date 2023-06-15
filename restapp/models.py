from django.db import models
import uuid
# Create your models here.


class restmodel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=255)
    place=models.CharField(max_length=255)
    phoneno=models.CharField(max_length=10)
    
    
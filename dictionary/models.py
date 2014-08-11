from django.db import models
from django.contrib.auth.models import User

class Record(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User)
    create_time = models.DateTimeField()
    keyword = models.CharField(max_length=16)
    last_lookup_time = models.DateTimeField()

    def __unicode__(self):
        return self.keyword
# Create your models here.

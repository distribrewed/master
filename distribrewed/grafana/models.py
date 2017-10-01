from django.contrib.postgres.fields import HStoreField, ArrayField
from django.db import models


# Create your models here.

class Alert(models.Model):
    title = models.CharField(max_length=50, null=True)
    ruleId = models.IntegerField(null=True)
    ruleName = models.CharField(max_length=200, null=True)
    ruleUrl = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=10, null=True)
    imageUrl = models.CharField(max_length=200, null=True)
    message = models.CharField(max_length=300, null=True)
    evalMatches = ArrayField(
        HStoreField(),
        null=True
    )

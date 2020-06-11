from django.db import models

# Create your models here.
class Ppl(models.Model):
    name = models.CharField(max_length=50)
    sid = models.CharField(max_length=50, unique = True)
    grade = models.CharField(max_length=50)
    pnum = models.CharField(max_length=50)
    rnum = models.CharField(max_length=50)
    lineuid = models.CharField(max_length=50)
from django.db import models

class Pair(models.Model):

    programmer_one = models.CharField(max_length=200)
    programmer_two = models.CharField(max_length=200)
    times = models.IntegerField(default=0)

    def __unicode__(self):
        return u"%s %s %d" % (self.programmer_one, self.programmer_two, self.times)

class Programmer(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

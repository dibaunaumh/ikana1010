from django.db import models

DEFAULT_DATA_SOURCE = "Twitter"

class Person(models.Model):
    username = models.CharField(max_length=500, unique=True, db_index=True)
    external_id = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    profile = models.CharField(max_length=1000, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    picture = models.URLField(null=True, blank=True)
    location_string = models.CharField(max_length=200, null=True, blank=True)
    location_wkt = models.CharField(max_length=200, null=True, blank=True)
    data_source = models.CharField(max_length=100, default=DEFAULT_DATA_SOURCE)
    
    
    def __unicode__(self):
        return self.username
    
    

class Message(models.Model):
    external_url = models.URLField(null=True, blank=True)
    person = models.ForeignKey(Person)
    contents = models.CharField(max_length=4000)
    location_string = models.CharField(max_length=200, null=True, blank=True)
    location_wkt = models.CharField(max_length=200, null=True, blank=True)
    data_source = models.CharField(max_length=100, default=DEFAULT_DATA_SOURCE)
    posted_at = models.DateTimeField(auto_now_add=True)
    pushed = models.BooleanField(default=False, help_text="Whether the message was pushed to the match engine")
    
    
    def __unicode__(self):
        return "%s: %s" % (self.person.username, self.contents)
from django.contrib.gis.db import models

SOURCES = (("TW", "Twitter"), ("FB", "FaceBook"), ("FL", "Flickr"))

class Person(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
class DataSource(models.Model):
    name = models.CharField(max_length=2, choices=SOURCES)
    
    def __unicode__(self):
        return self.name
    
class Message(models.Model):
    #External message ID
    external_id = models.CharField(max_length=100, null=True, blank=True)
    #Message contents
    contents = models.CharField(max_length=4000, db_index=True)
    #User
    user = models.ForeignKey(Person, related_name="messages")
    #Message data source
    source = models.ForeignKey(DataSource, related_name="messages")
    #Last message update
    last_update = models.DateTimeField(auto_now=True)
    #Message location (WTK format)
    location = models.PointField()
    #Message creation time
    created_at = models.DateTimeField(null=True, blank=True)
    
    def __unicode__(self):
        return self.contents
    
    
class Concept(models.Model):
    name = models.CharField(max_length=500)
    #Related persons
    persons = models.ManyToManyField(Person, through="ConceptAppearance", related_name="concepts")
    
    def __unicode__(self):
        return self.name
    
    
class ConceptAppearance(models.Model):
    message = models.ForeignKey(Message, related_name="concepts")
    concept = models.ForeignKey(Concept, related_name="appearances")
    person = models.ForeignKey(Person, related_name="appearances")
    
    def __unicode__(self):
        return "Concept %s appeared in message %s" % (self.concept, self.message)
    

from django.contrib.gis.db import models

SOURCES = ((0, "Twitter"), (1, "FaceBook"), (3, "Flickr"))

class Message(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    contents = models.CharField(max_length=4000, db_index=True)
    user_name = models.CharField(max_length=200, null=True, blank=True)
    source = models.IntegerField(default=0, choices=SOURCES)
    location = models.PointField()
    created_at = models.DateTimeField(null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.contents
    
    
class Concept(models.Model):
    name = models.CharField(max_length=500)
    
    def __unicode__(self):
        return self.name
    
    
class ConceptAppearance(models.Model):
    message = models.ForeignKey(Message, related_name="concepts")
    concept = models.ForeignKey(Concept, related_name="appearances")
    
    def __unicode__(self):
        return "Concept %s appeared in message %s" % (self.concept, self.message)
    

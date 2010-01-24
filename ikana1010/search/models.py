from django.contrib.gis.db import models


class DataSource(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
    

class Person(models.Model):
    username = models.CharField(max_length=500, unique=True, db_index=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    external_id = models.CharField(max_length=500, null=True, blank=True)
    profile = models.CharField(max_length=1000, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    picture = models.URLField(null=True, blank=True)
    source = models.ForeignKey(DataSource, related_name="persons")
    
     
    
    def __unicode__(self):
        return self.name
    

    
class Message(models.Model):
    #External message ID
    external_id = models.CharField(max_length=100, null=True, blank=True)
    #Message URL
    external_url = models.URLField(null=True, blank=True)
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
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.contents
    
    
    def get_x(self):
        return self.location.get_x()
    
    def get_y(self):
        return self.location.get_y()
    
    
    
    
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
    
    
MATCH_RATING_CHOICES = ((-2, "Completely off"),
                        (-1, "Not likely"),
                        (0, "Just random"),
                        (1, "To some extent"),
                        (2, "Indeed a match"),
                        )
    
class Match(models.Model):
    person1 = models.ForeignKey(Person, related_name="from_matches")
    person2 = models.ForeignKey(Person, related_name="to_matches")
    score = models.IntegerField(null=True, blank=True, help_text="Score of estimated match quality")
    common_concepts = models.CharField(max_length=1000, null=True, blank=True, help_text="Common concepts associated with both persons")
    notified = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)
    rated = models.IntegerField(default=0, choices=MATCH_RATING_CHOICES, help_text="Feedback received by match targets on match quality")
    
    
    def __unicode__(self):
        return u"Match between %s and %s" % (person1, person2)
    

from celery.task import Task
from celery.registry import tasks
from django.conf import settings
from search.models import *
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D 
from django.db.models.signals import post_save
import twitter


class DetectMatch(Task):

    def run(self, concept_appearance, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Detecting matches based on Concept Appearance: %s" % concept_appearance)
        # find all near-by concept appearances of this concept
        location = concept_appearance.message.location
        distance = settings.DISTANCE_THRESHOLD
        nearby_appearances = ConceptAppearance.objects.filter(concept=concept_appearance.concept).filter(message__location__distance_lte=(location, D(km=distance)))
        
        # collect the persons related to these concept appearances (exclude the person of the given concept appearance)
        if len(nearby_appearances) > 0:
            persons = set([ca.person for ca in nearby_appearances if ca.person.id != concept_appearance.person.id])
        
            # invoke a CheckMatchCandidate task to check out these persons
            for p in persons:
                CheckMatchCandidate.delay(concept_appearance.person, p)
        
        return True
    
    
tasks.register(DetectMatch)



class CheckMatchCandidate(Task):

    def run(self, person1, person2, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("*********************")
        logger.info("Check whether a match exists between: %s and %s" % (person1.username, person2.username))
        # get the list of concepts of each person
        p1_concepts = set(Concept.objects.filter(persons=person1))
        p2_concepts = set(Concept.objects.filter(persons=person2))
        
        # get the intersection of concepts
        common_concepts = p1_concepts.intersection(p2_concepts)
        # if its size is greater than the threshold, Bingo! create a Match entity
        if len(common_concepts) > settings.SCORE_TRESHOLD:
            logger.info("#######################   JACKPOT   #######################")
            logger.info("Found a match between: %s and %s" % (person1.username, person2.username))
            match = Match()
            match.person1 = person1
            match.person2 = person2
            match.score = len(common_concepts)
            match.common_concepts = ",".join([c.name for c in common_concepts])
            match.save()
            
        return True
    
    
tasks.register(CheckMatchCandidate)



class SendNotification(Task):

    def run(self, match, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Notify the users %s and %s about a match between them." % (match.person1.username, match.person2.username))
        notification_text = "Found interests match between @%s & @%s: %s" % (match.person1.username, match.person2.username, match.get_absolute_url())
        try:
            client = twitter.Api(username=settings.TWITTER_USER, password=settings.TWITTER_PASSWORD)
            status = client.PostUpdate(notification_text)
        except:
            logger.error("Failed to send notification about a match (%d)" % match.id)
        return True
    
    
    
def notify_match(sender, instance, **kwargs):
    SendNotification.delay(instance)
    
    
post_save.connect(notify_match, sender=Match)

tasks.register(SendNotification)
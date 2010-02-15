from rdflib import Namespace
from rdfalchemy import rdfSubject
from rdfalchemy.descriptors import *
from rdfalchemy.sesame2 import SesameGraph

matching = Namespace("http://www.ikana1010.com/matching.owl#")

rdfSubject.db = SesameGraph('http://localhost:8080/openrdf-sesame/repositories/ikana1010')

# Select all Person objects HOWTO
# objects = Person.filter_by()
# obj_set = set([item for item in objects])
# print objects

# Add Person's object HOWTO
# rdfSubject.db.add((URIRef("%(ns)s%(name)s" % {'ns' : matching, 'name' : 'person_id'}), RDF.type, matching.Person))

class Person(rdfSubject):
    rdf_type = matching.Person
    
class Concept(rdfSubject):
    rdf_type = matching.Concept
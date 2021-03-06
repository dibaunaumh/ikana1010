from django.contrib import admin
from models import *

class MessageAdmin(admin.ModelAdmin):
    list_display = ["contents", "user", "source", "location", "created_at"]
    search_fields = ["contents", "user"]
    list_filter = ["source",]
    date_hierarchy = "created_at"


class ConceptAdmin(admin.ModelAdmin):
    pass

class ConceptAppearanceAdmin(admin.ModelAdmin):
    pass

class PersonAdmin(admin.ModelAdmin):
    search_fields = ['name', 'username', 'profile']

class DataSourceAdmin(admin.ModelAdmin):
    pass

class MatchAdmin(admin.ModelAdmin):
    list_display = ["person1", "person2", "score", "common_concepts"]


admin.site.register(Person, PersonAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Concept, ConceptAdmin)
admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(ConceptAppearance, ConceptAppearanceAdmin)
admin.site.register(Match, MatchAdmin)
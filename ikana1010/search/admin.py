from django.contrib import admin
from models import *

class MessageAdmin(admin.ModelAdmin):
    list_display = ["contents", "user", "source", "created_at"]
    search_fields = ["contents", "user"]
    list_filter = ["source", "user"]


class ConceptAdmin(admin.ModelAdmin):
    pass

class ConceptAppearanceAdmin(admin.ModelAdmin):
    pass

class PersonAdmin(admin.ModelAdmin):
    pass

class DataSourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Person, PersonAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Concept, ConceptAdmin)
admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(ConceptAppearance, ConceptAppearanceAdmin)

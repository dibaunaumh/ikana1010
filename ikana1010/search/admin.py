from django.contrib import admin
from models import *

class MessageAdmin(admin.ModelAdmin):
    list_display = ["user_name", "contents", "source", "created_at"]
    search_fields = ["user_name", "contents"]
    list_filter = ["user_name", "source"]


class ConceptAdmin(admin.ModelAdmin):
    pass


class ConceptAppearanceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Message, MessageAdmin)
admin.site.register(Concept, ConceptAdmin)
admin.site.register(ConceptAppearance, ConceptAppearanceAdmin)

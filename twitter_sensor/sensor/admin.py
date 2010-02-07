from models import *
from django.contrib import admin



class PersonAdmin(admin.ModelAdmin):
    list_display = ["username", "location_string", "location_wkt", "picture"]
    search_fields = ["username", "name", "location_string", "location_wkt", "data_source"]
    list_filter = ["data_source", "location_string"]

admin.site.register(Person, PersonAdmin)



class MessageAdmin(admin.ModelAdmin):
    list_display = ["contents", "person", "location_string", "location_wkt", "data_source", "posted_at"]
    search_fields = ["contents", "location_string", "location_wkt", "data_source"]
    list_filter = ["data_source", "pushed"]
    date_hierarchy = "posted_at"

admin.site.register(Message, MessageAdmin)
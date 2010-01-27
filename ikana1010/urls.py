from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^ikana1010/', include('ikana1010.foo.urls')),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}), # serve static content. only for development.


    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^search/', 'ikana1010.search.views.search'),    
    
    (r'^receive_messages/', 'ikana1010.search.views.receive_messages'),
    
    (r'^match/(?P<match_id>\d+)/', 'ikana1010.search.views.view_match'),
    
    (r'^', 'ikana1010.search.views.home'),    
)

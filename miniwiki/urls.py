from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

PAGE_RE = r'\w+'

urlpatterns = patterns('',
    url(r'^$', 'miniwiki.views.home'),

    url(r"^login$", "miniwiki.views.user_login", name = "miniwiki_login"),
    url(r"^register$", "miniwiki.views.user_register", name = "miniwiki_register"),
    url(r"^logout$", "miniwiki.views.user_logout", name = "miniwiki_logout"),
    url(r"^profile$", "miniwiki.views.user_profile", name = "miniwiki_profile"),

    url(r'^(' + PAGE_RE + ')$', 'miniwiki.views.page', name = 'miniwiki_view'),
    url(r'^_edit/(' + PAGE_RE + ')$', 'miniwiki.views.edit', name = 'miniwiki_edit'),
    url(r'^_history/(' + PAGE_RE + ')$', 'miniwiki.views.history', name = 'miniwiki_history'),



    # Examples:
    # url(r'^$', 'miniwiki.views.home', name='home'),
    # url(r'^miniwiki/', include('miniwiki.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

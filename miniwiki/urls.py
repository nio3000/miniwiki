from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

PAGE_RE = r'\w+'

urlpatterns = patterns('',
    url(r'^$', 'miniwiki.views.home'),
    url(r'^(' + PAGE_RE + ')$', 'miniwiki.views.page', name='miniwiki_view'),
    url(r'^_edit/(' + PAGE_RE + ')$', 'miniwiki.views.edit', name='miniwiki_edit'),

    # Examples:
    # url(r'^$', 'miniwiki.views.home', name='home'),
    # url(r'^miniwiki/', include('miniwiki.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

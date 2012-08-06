from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from miniwiki.models import Page

from wiki import wikify

def home(request):
    return HttpResponseRedirect(reverse('miniwiki.views.page', args=('FrontPage',)))

def page(request, page_name = "FrontPage"):
    version = -1
    if 'version' in request.GET and request.GET['version'].isdigit():
        version = int(request.GET['version'])
        page_qs = Page.objects.filter(title=page_name, version=version)
    else:
        page_qs = Page.objects.filter(title=page_name).order_by('-version')

    if not page_qs.count():
        return HttpResponseRedirect(reverse('miniwiki.views.edit', args=(page_name,)))
    else:
        page = page_qs[0]

    return render_to_response('page.html', {'page_name': page_name, 'content': wikify(page.content), 'version': page.version})

def history(request, page_name = "FrontPage"):
    pages = Page.objects.filter(title=page_name).order_by('-version')
    return render_to_response('_history.html', {'page_name': page_name, 'pages': pages})

def edit(request, page_name):
    notice_message = None
    version = -1
    content = 'This page does not exist yet!'

    if 'version' in request.GET and request.GET['version'].isdigit():
        version = int(request.GET['version'])
        orig_page_qs = Page.objects.filter(title=page_name, version=version)
    else:
        orig_page_qs = Page.objects.filter(title=page_name).order_by('-version')

    if orig_page_qs.count():
        orig_page = orig_page_qs[0]
    else:
        version = 0
        orig_page = None

    if orig_page:
        content = orig_page.content
        version = orig_page.version

    if "POST" == request.method:
        content = request.POST['content']
        page = Page(title=page_name)

        page.version = 1 + Page.objects.filter(title=page_name).count()
        page.content = content
        page.save()

        version = page.version
        notice_message = "Changes saved!"

    return render_to_response('_edit.html',
                              {'page_name': page_name, 'content': content, 'version': version, 'notice_message': notice_message},
                              context_instance=RequestContext(request))
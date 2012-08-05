from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from miniwiki.models import Page

from wiki import wikify

def home(request):
    return HttpResponseRedirect(reverse('miniwiki.views.page', args=('FrontPage',)))

def page(request, page_name = "FrontPage"):
    page_qs = Page.objects.filter(title=page_name)
    if not page_qs.count():
        return HttpResponseRedirect(reverse('miniwiki.views.edit', args=(page_name,)))
    else:
        page = page_qs.get()

    return render_to_response('page.html', {'page_name': page_name, 'content': wikify(page.content)})

def edit(request, page_name):
    notification = ''
    content = 'This page does not exist yet!'
    # Fetch existing article, if any
    try:
        page = Page.objects.filter(title=page_name).get()
    except Page.DoesNotExist:
        page = None

    if page:
        content = page.content

    if "POST" == request.method:
        content = request.POST['content']
        if not page:
            page = Page(title=page_name)
        page.content = content
        page.save()

        notification = "Changes saved!"

    return render_to_response('_edit.html',
                              {'page_name': page_name, 'content': content, 'notification': notification},
                              context_instance=RequestContext(request))
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

    return render_to_response('page.html', {'page_name': page_name, 'content': wikify(page.content), 'version': page.version}, context_instance=RequestContext(request))

def history(request, page_name = "FrontPage"):
    pages = Page.objects.filter(title=page_name).order_by('-version')
    return render_to_response('_history.html', {'page_name': page_name, 'pages': pages}, context_instance=RequestContext(request))

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

        if request.user.is_authenticated():
            page.author = request.user
        else:
            page.author_ip = request.META['REMOTE_ADDR']

        page.save()

        version = page.version
        notice_message = "Changes saved!"

    return render_to_response('_edit.html',
                              {'page_name': page_name, 'content': content, 'version': version, 'notice_message': notice_message},
                              context_instance=RequestContext(request))

def user_register(request):
    if "POST" == request.method:
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        try:
            u = User.objects.get(username = username)
        except User.DoesNotExist:
            u = None

        params = {"username": username, "email": email}

        if u:
            params["error"] = "Username invalid"
            return render_to_response("register.html", params, context_instance=RequestContext(request))

        user = User.objects.create_user(username, email, password)
        user = authenticate(username = username, password = password)

        # Authenticate user.
        login(request, user)

        return HttpResponseRedirect(reverse("miniwiki.views.home"))

    return render_to_response("register.html", context_instance=RequestContext(request))

def user_login(request):
    if "POST" == request.method:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("miniwiki.views.home"))
        else:
            return render_to_response("login.html", {"username": username }, context_instance=RequestContext(request))

    return render_to_response('login.html', context_instance=RequestContext(request))

# @login_required(login_url='/login')
def user_profile(request):
    error = ""
    if "POST" == request.method:
        password = request.POST["password"]
        verif = request.POST["verif"]

        if len(password) >= 4 and password == verif:
            request.user.set_password(password)
            request.user.save()
            error = "Password changed!"
        else:
            error = "Invalid password"

    return render_to_response('profile.html', {"error": error}, context_instance=RequestContext(request))

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("miniwiki.views.home"))
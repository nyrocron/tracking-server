# Copyright 2015 Florian Tautz
# see LICENSE in the project root for licensing information

import json
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from tracker.models import TrackingSession, TrackedPosition, \
    TrackingKey
from tracking import settings


def authenticate_view_session(function=None, allow_viewkey=True):
    def decorator(fn):
        def inner(request, session_id, view_key=None, *args, **kwargs):
            session = get_object_or_404(TrackingSession, id=session_id)
            request.viewkey = view_key
            if allow_viewkey and view_key is not None:
                if session.viewkey != view_key:
                    return HttpResponseForbidden()
            elif not request.user.is_authenticated() or session.user != request.user:
                return redirect('{0}?next={1}'.format(settings.LOGIN_URL, request.path))
            request.tracking_session = session
            return fn(request, *args, **kwargs)
        return inner
    if function:
        return decorator(function)
    return decorator


def authenticate_tracking_session(function=None, allow_trackingkey=True):
    def decorator(fn):
        def inner(request, session_id, tracking_key=None, *args, **kwargs):
            session = get_object_or_404(TrackingSession, id=session_id)
            if allow_trackingkey and tracking_key is not None:
                if session.user.trackingkey.key != tracking_key:
                    return HttpResponseForbidden()
            elif not request.user.is_authenticated() or session.user != request.user:
                return redirect('{0}?next={1}'.format(settings.LOGIN_URL,
                                                      request.path))
            if not session.active:
                return HttpResponseForbidden('session is finished')
            request.tracking_session = session
            return fn(request, *args, **kwargs)
        return inner
    if function:
        return decorator(function)
    return decorator


def index(request):
    return render(request, 'index.html')


@login_required
def log_out(request):
    logout(request)
    return redirect('index')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            TrackingKey.create_key(new_user)
            return redirect('index')

    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def user_session_list(request):
    return render(request, 'session_list.html', {
        'session_list': request.user.trackingsession_set.order_by('-id'),
    })


@authenticate_view_session
def session(request):
    return render(request, 'session.html', {
        'session': request.tracking_session,
        'view_key': request.viewkey
    })


@authenticate_view_session(allow_viewkey=False)
def session_gpx(request):
    response = HttpResponse(request.tracking_session.as_gpx(),
                            content_type='application/gpx+xml')
    response['Content-Disposition'] = 'attachment; filename={0}.gpx'.format(
        request.tracking_session.title())
    return response


@authenticate_view_session(allow_viewkey=False)
def session_clean(request):
    request.tracking_session.clean_points()
    return redirect('user_session_list')


@authenticate_view_session(allow_viewkey=False)
def session_delete(request):
    request.tracking_session.delete()
    return redirect('user_session_list')


@authenticate_view_session
def session_data(request, since=None):
    return HttpResponse(request.tracking_session.as_json(since),
                        content_type='application/json')


def session_new(request, tracking_key):
    tk = get_object_or_404(TrackingKey, key=tracking_key)
    sess = TrackingSession.create_session(tk.user)
    return HttpResponse('{0},{1}'.format(sess.id, sess.viewkey))


@csrf_exempt
@require_POST
@authenticate_tracking_session
def track(request):
    for position in json.loads(request.body.decode('utf-8')):
        tp = TrackedPosition(session=request.tracking_session, **position)
        tp.save()
    return HttpResponse('ok')


@login_required
def tracking_key(request, action=None):
    if action == 'new':
        request.user.trackingkey.renew()

    return render(request, 'tracking_key.html', {
        'tracking_key': request.user.trackingkey
    })


@authenticate_tracking_session
def session_finish(request):
    request.tracking_session.finish()
    return HttpResponse("ok")

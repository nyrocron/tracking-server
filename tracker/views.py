from django import forms
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from tracker.forms import RegistrationForm

from tracker.models import TrackingSession, ViewKey, TrackedPosition, \
    TrackingKey
from tracking import settings


def auth_tracking_session(func):
    def inner(request, session_id, view_key=None, *args, **kwargs):
        session = get_object_or_404(TrackingSession, id=session_id)
        if view_key is not None:
            if not session.viewkey_set.get(key=view_key):
                return HttpResponseForbidden()
        elif not request.user.is_authenticated():
            return redirect('{0}?next={1}'.format(settings.LOGIN_URL, request.path))
        request.tracking_session = session
        return func(request, *args, **kwargs)
    return inner


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
            return redirect('index')

    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def viewkey_session_list(request, view_key):
    viewkey_object = get_object_or_404(ViewKey, key=view_key)
    return render(request, 'session_list.html', {
        'view_key': view_key,
        'session_list': viewkey_object.sessions.all(),
    })


@login_required
def user_session_list(request):
    return render(request, 'session_list.html', {
        'session_list': request.user.trackingsession_set.all(),
    })


@auth_tracking_session
def session(request):
    return render(request, 'session.html', {
        'session_id': request.tracking_session.id,
        'start_time': request.tracking_session.start_time,
    })


@auth_tracking_session
def session_data(request):
    return HttpResponse(request.tracking_session.as_json(),
                        content_type='application/json')


@csrf_exempt
def session_new(request, tracking_key):
    tk = get_object_or_404(TrackingKey, key=tracking_key)
    sess = TrackingSession.create_session(tk.user)
    return HttpResponse(sess.id)


@csrf_exempt
@require_POST
def track(request, tracking_key, session_id):
    tk = get_object_or_404(TrackingKey, key=tracking_key)
    session = get_object_or_404(TrackingSession, id=session_id)
    if tk.user_id != session.user_id:
        return HttpResponseForbidden()

    tp = TrackedPosition.from_json(session, request.body.decode('utf-8'))
    return HttpResponse(tp.id)


@login_required
def tracking_keys(request, action=None):
    if action == 'new':
        TrackingKey.create_key(request.user)

    return render(request, 'tracking_key.html', {
        'tracking_key': request.user.trackingkey
    })

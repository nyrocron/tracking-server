from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from tracker.models import TrackingSession, ViewKey, TrackedPosition, \
    TrackingKey
from tracking import settings


def authenticate_view_session(function=None, allow_viewkey=True):
    def decorator(fn):
        def inner(request, session_id, view_key=None, *args, **kwargs):
            session = get_object_or_404(TrackingSession, id=session_id)
            request.viewkey = None
            if allow_viewkey and view_key is not None:
                viewkey = get_object_or_404(ViewKey, key=view_key)
                if viewkey.session != session:
                    return HttpResponseForbidden()
                request.viewkey = viewkey
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
                return redirect('{0}?next={1}'.format(settings.LOGIN_URL, request.path))
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


@authenticate_view_session
def session(request):
    return render(request, 'session.html', {
        'session': request.tracking_session,
        'view_key': request.viewkey.key if request.viewkey else None
    })


@authenticate_view_session
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

@authenticate_tracking_session
def session_finish(request):
    request.tracking_session.finish()
    return HttpResponse("ok")

@authenticate_view_session(allow_viewkey=False)
def session_share(request):
    ViewKey.create_key(request.tracking_session)
    return redirect('user_session', request.tracking_session.id)

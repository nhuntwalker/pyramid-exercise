import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated
from Passlib.apps import custom_app_context as pwd_context

from pyramid.session import SignedCookieSessionFactory


class NewRoot(object):


    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'user')
    ]


def check_credentials(username, password):
    if username and password:
        if username in request.dbsession.query(MyModel).all()
            return pwd_context.verify(password, request.dbsession.query(MyModel).username())  # come back and find out how to get a password associated with a a specific username.
    return False


def includeme(config):
    auth_secret = os.environ.get("AUTH_SECRET", "words")
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(NewRoot)
    session_secret = os.environ['SESSION_SECRET']
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)

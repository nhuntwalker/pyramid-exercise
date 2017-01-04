from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel

from pyramid.httpexceptions import HTTPFound
from pyramid_gist.security import check_credentials
from pyramid.security import remember, forget
from passlib.apps import custom_app_contex as pwd_context


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    try:
        query = request.dbsession.query(MyModel)
        entries = query.all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'entries': entries}


@view_config(route_name='register', renderer='../templates/register.jinja2')
def register_view(request):
    try:
        if request.method == "POST":
            new_model = MyModel(username=request.POST['username'],
                                password=pwd_context.hash(request.POST['password']),
                                email=request.POST['email'],
                                fname=request.POST['fname'],
                                lname=request.POST['lname'],
                                ffood=request.POST['ffood']
                                )
            request.dbsession.add(new_model)
            return HTTPFound(location=request.route_url('home'))
        return {}
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='view', renderer='../templates/view.jinja2', permission="user")
def view_view(request):
    try:
        entry_id = int(request.matchdict['id'])
        query = request.dbsession.query(MyModel)
        entries = query.get(entry_id)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {"entries": entries}


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login_view(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            auth_head = remember(request, username)
            return HTTPFound(request.route_url('home'), headers=auth_head)
    return {}


@view_config(route_name='logout')
def logout_view(request):
    auth_head = forget(request)
    return HTTPFound(request.route_url('home'), headers=auth_head)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramid-gist_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

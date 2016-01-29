# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

import parse
import links

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    plots = UL(LI(A("[Barchart] Total score per over", _href=links.get(1))), 
               LI(A("[Barchart] Runs made per over", _href=links.get(2))),
               LI(A("[Line] Total score per over", _href=links.get(3))),
               LI(A("[Line] Runs made per over", _href=links.get(4))), 
               LI(A("[Barchart] Average runs per over", _href=links.get(5))))

    title = H1("Plots")
    body = DIV(title, plots, _style="margin-left: 5em")
    return dict(body=body)

def line():
    data_url = URL("default", "get_matches", extension="json", \
                            vars=dict(type=request.vars.get("type", "1")))
    return dict(data_url=data_url)

def overwise():
    data_url = URL("default", "get_matches", extension="json", \
                            vars=dict(type=request.vars.get("type", "1")))
    return dict(data_url=data_url)

def average():
    APO = parse.get_average_json(request.folder)
    return dict(APO=APO)

def get_matches():
    plot_type = request.vars.get("type", 1)
    final_json = parse.get_match_json(request.folder, int(plot_type))
    return dict(matches=final_json)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()



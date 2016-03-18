# -*- coding: utf-8 -*-
import parse
import links

# -----------------------------------------------------------------------------
def index():
    plots = UL(LI(A("[Barchart] Total score per over", _href=links.get(1))),
               LI(A("[Barchart] Runs made per over", _href=links.get(2))),
               LI(A("[Line] Total score per over", _href=links.get(3))),
               LI(A("[Line] Runs made per over", _href=links.get(4))),
               LI(A("[Barchart] Average runs per over", _href=links.get(5))),
               LI(A("[Line] Wickets per 5 over", _href=links.get(6))),
               LI(A("[Line] Successful chases", _href=URL("default",
                                                          "allwins"))))

    title = H1("Plots")
    body = DIV(title, plots, _style="margin-left: 5em")
    return dict(body=body)

# -----------------------------------------------------------------------------
def line():
    data_url = URL("default",
                   "get_matches",
                   extension="json",
                   vars=dict(type=request.vars.get("type", "1")))
    return dict(data_url=data_url)

# -----------------------------------------------------------------------------
def overwise():
    data_url = URL("default",
                   "get_matches",
                   extension="json",
                   vars=dict(type=request.vars.get("type", "1")))
    return dict(data_url=data_url)

# -----------------------------------------------------------------------------
def average():
    APO = parse.get_average_json(request.folder)
    return dict(APO=APO)

# -----------------------------------------------------------------------------
def get_matches():
    plot_type = request.vars.get("type", 1)
    final_json = parse.get_match_json(request.folder, int(plot_type))
    return dict(matches=final_json)

# -----------------------------------------------------------------------------
def allwins():
    return dict(allwins=parse.get_allwins_json(request.folder))

# -----------------------------------------------------------------------------
def fow():
    """
        Fall of wickets in range of 5 overs in the chasing innings
    """

    final_json = parse.get_match_json(request.folder)
    final_fow = [0] * 10
    for match_id in final_json:
        overs = final_json[match_id]["overs"]
        wickets = [0] * 51
        for over in overs:
            wickets[int(over)] = overs[over]["wicket2"]
        new_wickets = [0] * 51
        for wicket in xrange(1, len(wickets)):
            if wickets[wicket] is None:
                break
            new_wickets[wicket] = wickets[wicket] - wickets[wicket - 1]
            if new_wickets[wicket] < 0:
                new_wickets[wicket] = 0
        i = 1
        fow = []
        while i <= 46:
            fow.append(sum(new_wickets[i:i + 5]))
            i += 5
        final_fow = map(lambda x, y: x + y, final_fow, fow)

    final_fow = map(lambda x: x * 1.0 / len(final_json), final_fow)
    return dict(fow=final_fow)

# -----------------------------------------------------------------------------
def run():
    print request.post_vars
    return dict()

# -----------------------------------------------------------------------------
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



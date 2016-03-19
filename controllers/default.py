# -*- coding: utf-8 -*-
import parse
import links
import os, csv
import math
import cPickle as pickle
import operator

# -----------------------------------------------------------------------------
def index():
    redirect(URL("default", "run"))
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

    data = {}
    if request.post_vars:
        overs = float(request.post_vars.overs)
        teamA = request.post_vars.teama
        teamB = request.post_vars.teamb
        target = int(request.post_vars.target)
        wickets = int(request.post_vars.wickets)
        runs = int(request.post_vars.runs)
        # Save over, find out possible upcoming bowlers
        _overs = int(math.ceil(overs))
        # Increase the number of overs to get the expected par score
        overs += 5
        overs = min(overs, 50.0)

        with open(os.path.join(request.folder,
                               "private",
                               "jayadevantable.csv"), "rb") as csvfile:
            row = list(csv.reader(csvfile, delimiter=','))
            for i in row[1:]:
                data[int(i[0])] = {"target": float(i[1]),
                                   "normal": i[2:]}
        # Get percentage
        percentage = ((overs * 1.0)/50.0) * 100.0
        if percentage >= math.floor(percentage) + 0.5:
            percentage = math.ceil(float(percentage))

        NS = float(data[int(percentage)]["normal"][wickets])/100.0

        parscore = math.ceil(NS * target)
        bowling_stats = pickle.load(
                            open(os.path.join(
                                    request.folder,
                                    "private",
                                    "bowling/teams_dict_2010.p"), "rb"))
        if _overs < 45:
            part1 = []
            part2 = []

            for ono in xrange(_overs, min(_overs + 5, 50)):
                # Sort the bowlers by freqency
                sb = sorted(bowling_stats[teamA][ono].items(),
                            key=operator.itemgetter(1),
                            reverse=True)
                sb = sb[:5]
                for bowler in sb:
                    part1.append(bowler[0])
            part1 = list(set(part1))

            for ono in xrange(_overs + 5, min(_overs + 10, 50)):
                # Sort the bowlers by freqency
                sb = sorted(bowling_stats[teamA][ono].items(),
                            key=operator.itemgetter(1),
                            reverse=True)
                sb = sb[:5]
                for bowler in sb:
                    part2.append(bowler[0])
            part2 = list(set(part2))

        else:
            part1 = []
            part2 = []
            for ono in xrange(_overs, min(_overs + 5, 50)):
                # Sort the bowlers by freqency
                sb = sorted(bowling_stats[teamA][ono].items(),
                            key=operator.itemgetter(1),
                            reverse=True)
                sb = sb[:5]
                for bowler in sb:
                    part1.append(bowler[0])
            part1 = list(set(part1))

        team_data = nn = None
        if session["team_data"]:
            team_data = session["team_data"]
        if session["nn"]:
            nn = session["nn"]
        if team_data is None or nn is None:
            team_data, nn = parse.train_data(request.folder)
            session["team_data"] = team_data
            session["nn"] = nn

        bowlers1 = bowlers2 = []
        for i in part1:
            cat = parse.get_bowler_class(team_data, nn, i, teamA, request.folder)
            if cat == -1:
                bowlers1.append((i, -1, -1))
            else:
                bowlers1.append((i, cat[0], cat[1]))
        for i in part2:
            cat = parse.get_bowler_class(team_data, nn, i, teamA, request.folder)
            if cat == -1:
                bowlers2.append((i, -1, -1))
            else:
                bowlers2.append((i, cat[0], cat[1]))
        print bowlers1, bowlers2

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



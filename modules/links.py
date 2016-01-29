from gluon.html import URL

def get(plot_type):
    
    # controller
    c = "default"
    # function
    f = ""
    # Request vars
    req_vars = {"type": 1}
    if plot_type == 1:
        f = "overwise"
    elif plot_type == 2:
        f = "overwise"
        req_vars["type"] = 2
    elif plot_type == 3:
        f = "line"
    elif plot_type == 4:
        f = "line"
        req_vars["type"] = 2
    elif plot_type == 5:
        f = "average"
    return URL(c, f, vars=req_vars)

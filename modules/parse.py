import os, csv

request_folder = None
all_matches = []
team_mappings = {}
matches_dir = None
CUTOFF = 310

# -----------------------------------------------------------------------------
def get_final_scores(records):

    total1 = 0
    total2 = 0

    for over_no, score1, score2 in records:
        if over_no == "Over":
            continue
        if score1 != "nil":
            total1 = int(score1.split("/")[0])
        if score2 != "nil":
            total2 = int(score2.split("/")[0])

    return total1, total2

# -----------------------------------------------------------------------------
def populate_team_names():

    f = open(os.path.join(request_folder,
                          "private",
                          "CompleteMatchDetails.csv"),
             "rb")
    matches = csv.reader(f)
    for match in matches:
        team_mappings[match[1]] = (match[-2], match[-1])
    f.close()

# -----------------------------------------------------------------------------
def run(req_folder):

    global request_folder, matches_dir
    request_folder = req_folder
    matches_dir = os.path.join(request_folder, "private", "csvs/")

    for root, dirs, files in os.walk(matches_dir):
        all_matches = files

    count = 0
    populate_team_names()
    for match in all_matches:

        match_id = match[:-4]
        f = open(matches_dir + match, "rb")
        overs = csv.reader(f)

        # Convention: somevar1 => somevar property for first innings
        #             somevar2 => somevar property for second innings
        total1, total2 = get_final_scores(list(overs))
        if total1 >= CUTOFF:
            count += 1
            print team_mappings[match_id][0], total1, team_mappings[match_id][1], total2
        f.close()

    return count

# -----------------------------------------------------------------------------
def get_match_json(req_folder):

    global request_folder, matches_dir

    request_folder = req_folder
    matches_dir = os.path.join(request_folder, "private", "csvs/")

    for root, dirs, files in os.walk(matches_dir):
        all_matches = files

    final_json = {}
    populate_team_names()

    for match in all_matches:

        match_id = match[:-4]
        f = open(matches_dir + match, "rb")
        overs = csv.reader(f)

        final_json[match_id] = {}
        this_match = final_json[match_id]

        this_match["team1"] = team_mappings[match_id][0]
        this_match["team2"] = team_mappings[match_id][1]
        this_match["overs"] = {}
        match_overs = this_match["overs"]

        total1 = 0
        total2 = 0

        for over_no, score1, score2 in overs:
            if over_no == "Over":
                continue

            tmp1 = score1.split("/")
            tmp2 = score2.split("/")

            if tmp1[0] != "nil":
                total1 = int(tmp1[0])
            if tmp2[0] != "nil":
                total2 = int(tmp2[0])

            if len(tmp1) == 1 and len(tmp2) > 1:
                match_overs[over_no] = {"score1": None,
                                        "score2": int(tmp2[0]),
                                        "wicket1": None,
                                        "wicket2": int(tmp2[1])}
            elif len(tmp2) == 1 and len(tmp1) > 1:
                match_overs[over_no] = {"score1": int(tmp1[0]),
                                        "score2": None,
                                        "wicket1": int(tmp1[1]),
                                        "wicket2": None}
            elif len(tmp1) <= 1 and len(tmp2) <= 1:
                match_overs[over_no] = {"score1": None,
                                        "score2": None,
                                        "wicket1": None,
                                        "wicket2": None}
            else:
                match_overs[over_no] = {"score1": int(tmp1[0]),
                                        "score2": int(tmp2[0]),
                                        "wicket1": int(tmp1[1]),
                                        "wicket2": int(tmp2[1])}

        final_json[match_id]["total1"] = total1
        final_json[match_id]["total2"] = total2

        if total1 < CUTOFF:
            del final_json[match_id]

    return final_json

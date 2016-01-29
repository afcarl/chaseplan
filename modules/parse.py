import os, csv, math

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
def get_match_json(req_folder, plot_type):

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

        # total = [TeamA total, TeamB total]
        total = [-1, -1]
        wickets = [-1, -1]
        last_over_score = [0, 0]
        rpo = [0, 0]

        for over_no, score1, score2 in overs:

            if over_no == "Over" or over_no == "-":
                # Over no = "-" ?
                continue

            tmp1 = score1.split("/")
            tmp2 = score2.split("/")

            flag = [0, 0]

            if tmp1[0] != "nil":
                total[0] = int(tmp1[0])
                wickets[0] = int(tmp1[1])
                # Valid Score
                flag[0] = 1
            if tmp2[0] != "nil":
                total[1] = int(tmp2[0])
                wickets[1] = int(tmp2[1])
                # Valid Score
                flag[1] = 1

            for i in xrange(0, 2):
                if flag[i] and plot_type == 1:
                    rpo[i] = total[i]
                elif flag[i] and plot_type == 2:
                    rpo[i] = total[i] - last_over_score[i]
                    last_over_score[i] = total[i]
                else:
                    rpo[i] = None

            match_overs[over_no] = {"score1": rpo[0],
                                    "score2": rpo[1],
                                    "wicket1": wickets[0] if flag[0] else None,
                                    "wicket2": wickets[1] if flag[1] else None}

        final_json[match_id]["total1"] = total[0]
        final_json[match_id]["total2"] = total[1]

        if total[0] < CUTOFF:
            del final_json[match_id]

    return final_json

# -----------------------------------------------------------------------------
def get_allwins_json(req_folder):

    global request_folder, matches_dir

    request_folder = req_folder
    matches_dir = os.path.join(request_folder, "private", "csvs/")

    for root, dirs, files in os.walk(matches_dir):
        all_matches = files

    # winning matches, team 2 chased a high total

    populate_team_names()

    # Runs per over
    all_wins = {"overs": dict(zip([i for i in xrange(1, 51)], [None]*50)),
                "no_of_matches": 0}

    for i in all_wins["overs"]:
        all_wins["overs"][i] = []

    for match in all_matches:

        match_id = match[:-4]
        f = open(matches_dir + match, "rb")
        overs = csv.reader(f)

        team1 = team_mappings[match_id][0]
        team2 = team_mappings[match_id][1]

        PO = dict(zip([i for i in xrange(1, 51)], [0]*50))

        # total = [TeamA total, TeamB total]
        total = [-1, -1]
        wickets = [-1, -1]
        last_over_score = [0, 0]

        for over_no, score1, score2 in overs:

            if over_no == "Over" or over_no == "-":
                # Over no = "-" ?
                continue

            tmp1 = score1.split("/")
            tmp2 = score2.split("/")

            flag = [0, 0]

            if tmp1[0] != "nil":
                total[0] = int(tmp1[0])
                wickets[0] = int(tmp1[1])
                # Valid Score
                flag[0] = 1
            if tmp2[0] != "nil":
                total[1] = int(tmp2[0])
                wickets[1] = int(tmp2[1])
                # Valid Score
                flag[1] = 1

            if flag[1]:
                PO[int(over_no)] = total[1] - last_over_score[1]
                last_over_score[1] = total[1]
            else:
                # Team2 WON OR ALL OUT
                PO[int(over_no)] = 0 # 0? or put average score ? like 6 ?

        if total[0] >= CUTOFF and total[1] >= total[0]:
            for o in xrange(1, 51):
                all_wins["overs"][o].append([match_id, team1, team2, PO[o]])
            all_wins["no_of_matches"] += 1

    return all_wins

# -----------------------------------------------------------------------------
def get_average_json(req_folder):

    global request_folder, matches_dir

    request_folder = req_folder
    matches_dir = os.path.join(request_folder, "private", "csvs/")

    for root, dirs, files in os.walk(matches_dir):
        all_matches = files

    populate_team_names()

    # Average runs per over
    APO = {"overs": dict(zip([i for i in xrange(1, 51)], [0]*50)),
           "no_of_matches": 0}

    for match in all_matches:

        match_id = match[:-4]
        f = open(matches_dir + match, "rb")
        overs = csv.reader(f)

        # total = [TeamA total, TeamB total]
        total = [-1, -1]
        wickets = [-1, -1]

        # Per Over
        PO = dict(zip([i for i in xrange(1, 51)], [0]*50))
        last_over_score = 0

        for over_no, score1, score2 in overs:

            if over_no == "Over" or over_no == "-":
                # Over no = "-" ?
                continue

            tmp1 = score1.split("/")
            tmp2 = score2.split("/")

            flag = [0, 0]

            if tmp1[0] != "nil":
                total[0] = int(tmp1[0])
                wickets[0] = int(tmp1[1])
                # Valid Score
                flag[0] = 1
            if tmp2[0] != "nil":
                total[1] = int(tmp2[0])
                wickets[1] = int(tmp2[1])
                # Valid Score
                flag[1] = 1

            if flag[1]:
                PO[int(over_no)] = total[1] - last_over_score
                last_over_score = total[1]
            else:
                # Team2 WON OR ALL OUT
                PO[int(over_no)] = 0 # 0? or put average score ? like 6 ?

        # Average overwise score
        if total[0] >= CUTOFF and total[1] >= total[0]:
            # TEAM2 WON, CHASED HIGH TOTAL
            for o in xrange(1, 51):
                APO["overs"][o] += PO[o]
            APO["no_of_matches"] += 1

    # CALCULATE AVERAGE
    for o in xrange(1, 51):
        APO["overs"][o] = int(math.ceil(float(APO["overs"][o])/APO["no_of_matches"]))

    return APO

import sys

# -----------------------------------------------------------------------------
def batting_heuristic(player):
    """
        Return a heuristic score for a particular batsman
    """
    score = player["strike_rate"] * 20 + \
            player["average"] * 200 + \
            player["sixes"] * 10 + \
            player["boundaries"] * 5 - \
            player["ducks"] * 10 + \
            player["not_out"] * 5 + \
            player["innings"] * 10 + \
            player["runs"] * 5 + \
            player["centuries"] * 20 + \
            player["half_centuries"] * 7
    return score

# -----------------------------------------------------------------------------
def batting(team):
    f = open("data/batting/" + team + ".csv")
    players = f.readlines()[1:]
    f.close()
    for player in players:
        line = player.strip("\r\n")
        line = line.replace("-", "0")
        line = line.replace("*", "")
        line = line.split(",")
        player_dict = {}
        player_dict["name"] = line[0]
        player_dict["matches"] = int(line[2])
        player_dict["innings"] = int(line[3])
        player_dict["not_out"] = int(line[4])
        player_dict["runs"] = int(line[5])
        player_dict["highest_score"] = int(line[6])
        player_dict["average"] = float(line[7])
        player_dict["balls_faced"] = int(line[8])
        player_dict["strike_rate"] = float(line[9])
        player_dict["centuries"] = int(line[10])
        player_dict["half_centuries"] = int(line[11])
        player_dict["ducks"] = int(line[12])
        player_dict["boundaries"] = int(line[13])
        player_dict["sixes"] = int(line[14])

        score = batting_heuristic(player_dict)
        print player_dict["name"], score

# -----------------------------------------------------------------------------
def bowling_heuristic(player):
    score = player["average"] * 20 - \
            player["economy"] * 50 + \
            player["4s"] * 100 + \
            player["5s"] * 500 + \
            player["maidens"] * 100 + \
            player["innings"] * 20 - \
            player["runs"] * 50 + \
            player["wickets"] * 100
    return score

# -----------------------------------------------------------------------------
def bowling(team):

    f = open("data/bowling/" + team + ".csv")
    players = f.readlines()[1:]
    f.close()
    for player in players:
        line = player.strip("\r\n")
        line = line.replace("-", "0")
        line = line.replace("*", "")
        line = line.split(",")
        player_dict = {}
        player_dict["name"] = line[0]
        player_dict["matches"] = int(line[2])
        player_dict["innings"] = int(line[3])
        player_dict["overs"] = float(line[4])
        player_dict["maidens"] = int(line[5])
        player_dict["runs"] = int(line[6])
        player_dict["wickets"] = int(line[7])
        player_dict["bbi"] = line[8]
        player_dict["average"] = float(line[9])
        player_dict["economy"] = float(line[10])
        player_dict["strike_rate"] = float(line[11])
        player_dict["4s"] = int(line[12])
        player_dict["5s"] = int(line[13])

        score = bowling_heuristic(player_dict)
        print player_dict["name"], score

# -----------------------------------------------------------------------------
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "Pass arguments..."
        sys.exit()

    team = sys.argv[1]
    bat_or_bowl = int(sys.argv[2])

    if bat_or_bowl == 1:
        batting(team)
    else:
        bowling(team)

import pandas as pd
import sys
from sknn.mlp import Classifier, Layer

Teams = ['Australia', 'Bangladesh', 'England', 'India', 'NewZealand', 'Pakistan', 'SouthAfrica', 'SriLanka', 'WestIndies', 'Zimbabwe']
Category = ['Batting', 'Bowling']
currentCat = "Bowling"

test_team = sys.argv[1]
teamData = {}

for team in Teams:
    # for category in Category:
    currentTeam = team
    currentCSVPath = '../' + 'Data/' + currentTeam + '/' + currentCat + '.csv'

    currentData = pd.read_csv(currentCSVPath)
    manualRating = []

    for player in range(0, currentData['Mat'].__len__()):
        if currentCat == "Batting":
            if currentData['HS'][player] == '-':
                currentData['HS'][player] = 0
            if currentData['BF'][player] == '-':
                currentData['BF'][player] = 0
            if currentData['100'][player] == '-':
                currentData['100'][player] = 0
            if currentData['50'][player] == '-':
                currentData['50'][player] = 0
            if currentData['0'][player] == '-':
                currentData['0'][player] = 0
        elif currentCat == "Bowling":
            if currentData['Overs'][player] == '-':
                currentData['Overs'][player] = 0
            if currentData['Mdns'][player] == '-':
                currentData['Mdns'][player] = 0
            if currentData['Wkts'][player] == '-':
                currentData['Wkts'][player] = 0
            if currentData['Econ'][player] == '-':
                currentData['Econ'][player] = 0
            if currentData['4'][player] == '-':
                currentData['4'][player] = 0
            if currentData['5'][player] == '-':
                currentData['5'][player] = 0
            if currentData['BBI'][player] == '-':
                currentData['BBI'][player] = 0
        if currentData['Mat'][player] == '-':
            currentData['Mat'][player] = 0
        if currentData['Ave'][player] == '-':
            currentData['Ave'][player] = 0
        if currentData['SR'][player] == '-':
            currentData['SR'][player] = 0
        if currentData['Inns'][player] == '-':
            currentData['Inns'][player] = 0
        if currentData['Runs'][player] == '-':
            currentData['Runs'][player] = 0

        if currentCat == "Batting":
            if int(currentData['Runs'][player]) >= 1700 or int(currentData['Inns'][player]) >= 60:
                manualRating.append(2)
            elif (int(currentData['Runs'][player]) < 1700 and int(currentData['Runs'][player]) >= 500) or (int(currentData['Inns'][player]) >= 40 and int(currentData['Inns'][player]) < 60):
                manualRating.append(1)
            else:
                manualRating.append(0)
        elif currentCat == "Bowling":
            if int(currentData['Wkts'][player]) >= 70 or float(currentData['Overs'][player]) >= 400:
                manualRating.append(2)
            elif (int(currentData['Wkts'][player]) < 70 and int(currentData['Wkts'][player]) >= 40) or (float(currentData['Overs'][player]) >= 150 and float(currentData['Overs'][player]) < 400):
                manualRating.append(1)
            else:
                manualRating.append(0)

    currentData['Rating'] = manualRating

    currentStatus = []
    lastPlayed = []

    for player in currentData['Span']:
        if player[-1] == '5':
            currentStatus.append('Yes')
            lastPlayed.append('Active')
        else:
            currentStatus.append('No')
            lastPlayed.append(player.split('-')[1])

    currentData['LastPlayed'] = lastPlayed

    teamData[team] = currentData

nn = Classifier(
    layers=[
        Layer("Rectifier", units=100, pieces=6),
        Layer("Softmax")],
    learning_rate=0.05,
    learning_rule='adadelta',
    n_iter=1000)

trainData = None

for team in teamData:
    if trainData is None:
        trainData = teamData[team]
    elif team != test_team:
        frames = [trainData, teamData[team]]

testData = teamData[test_team].as_matrix(['Runs', 'Inns', 'Ave', 'SR'])

y = trainData['Rating'].as_matrix()
trainData = trainData.as_matrix(['Runs', 'Inns', 'Ave', 'SR'])

nn.fit(trainData, y)

x = nn.predict(testData)
score = nn.score(testData, teamData[test_team]['Rating'].as_matrix())
for player in range(0, x.__len__()):
    print str(x[player])+": "+teamData[test_team]['Player'][player]+": "+str(teamData[test_team]['LastPlayed'][player])

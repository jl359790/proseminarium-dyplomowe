import re
from enum import Enum
class ROR(Enum):
    Buy = 0
    Hold = 1
    Sell = 2

def ReadROR(str):
    if str == 'Buy\n':
        return ROR.Buy
    if str == 'Buy':
        return ROR.Buy
    if str == 'Hold\n':
        return ROR.Hold
    if str == 'Hold':
        return ROR.Hold
    if str == 'Sell\n':
        return ROR.Sell
    if str == 'Sell':
        return ROR.Sell

def recommendationSplit(stockRecommendation):
    stockRecommendation = re.sub('{(.*)}', '\\1', stockRecommendation)
    recommendation = re.split(',', stockRecommendation)
    recommendation[0] = int(recommendation[0])
    recommendation[1] = ReadROR(recommendation[1])
    if (recommendation[2] != 'NA'):
        recommendation[2] = float(recommendation[2])
    recommendation[3] = int(recommendation[3])
    return recommendation
    
        
trainingFile = open('trainingData.csv', 'r')
trainingFile.readline() #there is a headline, we don't want it

expertsPoints = dict()

for i in range (0, 12234):
    stock = trainingFile.readline()
    split = re.split(';', stock)
    trueClass = ReadROR(split[2])
    stockRecommendations = re.findall('{[^}]*}', split[1])
    for j in range(0, len(stockRecommendations)):
        recommendation = recommendationSplit(stockRecommendations[j])
        if (trueClass == recommendation[1]):
            currentExpertPoints = expertsPoints.get(recommendation[0], 0)
            expertsPoints[recommendation[0]] = currentExpertPoints + recommendation[3] + 1

trainingFile.close()
testFile = open('testData.csv', 'r')
outputFile = open('predictions.csv', 'w')
testFile.readline() #there is a headline, we don't want it

for i in range (0, 7555):
    stock = testFile.readline()
    split = re.split(';', stock)
    stockRecommendations = re.findall('{[^}]*}', split[1])
    accSums = {ROR.Buy: 0.0, ROR.Hold: 0.0, ROR.Sell: 0.0}
    addedExperts = list()
    for j in range (0, len(stockRecommendations)):
        recommendation = recommendationSplit(stockRecommendations[j])
        if not (recommendation[0] in addedExperts):
            addedExperts.append(recommendation[0])
            accSums[recommendation[1]] += expertsPoints.get(recommendation[0], 0)
    max = ROR.Hold
    if (accSums[ROR.Buy] > accSums[max]):
        max = ROR.Buy
    if (accSums[ROR.Sell] > accSums[max]):
        max = ROR.Sell
    outputFile.write(max.name)
    outputFile.write('\n')
    
testFile.close()
outputFile.close()
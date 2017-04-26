from enum import Enum
class ROR(Enum):
	Buy = 0
	Hold = 1
	Sell = 2

def ReadROR(line):
	if line == "Buy\n":
		return ROR.Buy
	if line == "Buy":
		return ROR.Buy
	if line == "Hold\n":
		return ROR.Hold
	if line == "Hold":
		return ROR.Hold
	if line == "Sell\n":
		return ROR.Sell
	if line == "Sell":
		return ROR.Sell
	
X = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]	#rows - prediction, columns - truth
C = [[8, 4, 8], [1, 1, 1], [8, 4, 8]]
	
predictionsFile = open("predictions.csv", "r")
trueClassesFile = open("true_test_classes.csv", "r")

for i in range (0, 7555):

	predictionStr = predictionsFile.readline()
	prediction = ReadROR(predictionStr)
	trueClassStr = trueClassesFile.readline()
	trueClass = ReadROR(trueClassStr)
	X[prediction.value][trueClass.value] += 1

numerator = 0
denominator = 0
for i in range (0, 3):
	numerator += C[i][i] * X[i][i]
	for j in range (0, 3):
		denominator += C[i][j] * X[i][j]
		
ACC = numerator / denominator
print(ACC)
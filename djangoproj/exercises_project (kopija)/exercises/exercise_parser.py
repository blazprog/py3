class ExercisePart:
    QUESTION_PART, ANSWER_PART = range(2)
    def __init__(self, text, partType, partName):
        self.text = text
        self.partType = partType
        self.partName = partName
        self.userAnswer=""

    def __str__(self):
        return  self.text

    def setUserAnswer(self, value):
        self.userAnswer = value

    def __len__(self):
        return len(self.text)

def markUserAnswer(exercise_name,answer, exercisesList):
    for exercise in exercisesList:
        for part in exercise:
            if part.partName == exercise_name:
                part.setUserAnswer(answer)
                return

def parse(exerciseLines):
    lines = exerciseLines.split("\n")
    resultDisplay = []
    resultAnswers = {}
    a = 1
    prefix = "q"
    for i,line in enumerate(lines):
        line = line.strip()
        parts = line.split("#")
        temp_list = []
        for j, part in enumerate(parts):
            if j % 2:
                partType = ExercisePart.ANSWER_PART
                name_prefix = "a"
            else:
                partType = ExercisePart.QUESTION_PART
                name_prefix = "q"
            partName = "{0}-{1}.{2}".format(name_prefix,i+1, j+1)
            exercisePart = ExercisePart(part.strip(), partType, partName)
            temp_list.append(exercisePart)

            if partType == ExercisePart.ANSWER_PART:
                resultAnswers[partName] = exercisePart.text

        resultDisplay.append(temp_list)

    print("Vseh vrstic", len(resultDisplay))
    return resultDisplay, resultAnswers

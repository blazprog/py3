__author__ = 'blazko'
class ExercisePart:
    QUESTION_PART, ANSWER_PART = range(2)
    def __init__(self, text, partType, partName, hint=""):
        self.text = text
        self.hint=hint
        self.partType = partType
        self.partName = partName
        self.userAnswer=""

    def __str__(self):
        return  self.text

    def setUserAnswer(self, value):
        self.userAnswer = value

    def __len__(self):
        return len(self.text)

    def input_size(self):
        return self.__len__()

def markUserAnswer(exercise_name,answer, exercisesList):
    #Tu lahko preštejem pravilne in nepravilne odgovore
    """
    Funkcija zabeleži uporabnikov odgovor na vprašanje in vrne
    true/false glede na pravilnost odgovora
    """
    for exercise in exercisesList:
        for part in exercise:
            if part.partName == exercise_name:
                part.setUserAnswer(answer)
                if answer == part.text:
                    return True
                else:
                    return False
    return False

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
                #Če imama vprašanje tipa #namig, pravilen odgovor#
                #moram v html formi za vprašanje napisati namig
                if part.find(",") ==  -1:
                    hint=""
                else:
                    s = part.split(",")
                    hint = s[0].strip()
                    part = s[1].strip()
            else:
                partType = ExercisePart.QUESTION_PART
                name_prefix = "q"
                hint=""
            partName = "{0}-{1}.{2}".format(name_prefix,i+1, j+1)
            exercisePart = ExercisePart(part.strip(), partType, partName,hint)
            temp_list.append(exercisePart)

            if partType == ExercisePart.ANSWER_PART:
                resultAnswers[partName] = exercisePart.text

        resultDisplay.append(temp_list)
    return resultDisplay, resultAnswers

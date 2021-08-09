from os import path


def file_name(filePath):
    filePath = filePath.split("/")
    return (filePath[len(filePath) - 1]).split(".wcs")[0]


def read_solution_without_abducibles(solutionFilePath):
    readSolutionFile = open(solutionFilePath, 'r')
    lines = readSolutionFile.readlines()
    nextLine = False

    for line in lines:
        if nextLine:
            format_solution(line)
            break
        elif line.startswith("Answer:"):
            nextLine = True
        elif line.startswith("UNSATISFIABLE"):
            print("\nThe formula is UNSATISFIABLE")
            break
    readSolutionFile.close()


def read_solution_with_abducibles(solutionFilePath):
    readSolutionFile = open(solutionFilePath, 'r')
    lines = readSolutionFile.readlines()
    nextLineSolution = False
    setOfAllSolution = []

    for line in lines:
        if nextLineSolution:
            literals = [literal.replace("true(", "").replace("false(", "-").replace(")", "").strip()
                        for literal in line.split(' ')]
            setOfAllSolution.append(literals)
            nextLineSolution = False
        elif line.startswith("Answer:"):
            nextLineSolution = True
        elif line.startswith("UNSATISFIABLE"):
            print("\nThe formula is UNSATISFIABLE")
            break
    readSolutionFile.close()
    print(setOfAllSolution)
    return setOfAllSolution


def format_solution(solution):
    literals = [literal.strip() for literal in solution.split(' ')]
    positiveLiterals = []
    negativeLiterals = []
    print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
    for literal in literals:
        if literal.startswith('false'):
            negativeLiterals.append(literal.replace('false(', '').replace(")", ""))
        else:
            positiveLiterals.append(literal.replace('true(', '').replace(")", ""))
    if len(positiveLiterals) > 0:
        print("Positive literals are: " + ", ".join(positiveLiterals))
    else:
        print("There are no positive literals!")
    if len(negativeLiterals) > 0:
        print("Negative literals are: " + ", ".join(negativeLiterals))
    else:
        print("There are no negative literals!")
    print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")

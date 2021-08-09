from os import path
import itertools


def check_if_file_exists(filePath):
    if not path.exists(filePath):
        raise FileNotFoundError("Could not allocate the file!")


def execute_encoding(filePath, observation, supported, semantics):
    writeFilePath = filename_separator(filePath) + "-facts-and-rules.lp"
    factsFile = open(writeFilePath, "w+")
    mode = execution_mode(observation, supported)
    counter = 1
    definedAtoms = []
    bodyAtoms = []
    negatedPartRules = dict()
    trueAndFalseRules = ""
    trueRulesUnderK = ""

    with open(filePath, 'r') as file:
        for line in non_blank_and_non_comment_lines(file):
            rule = line.split(":-")
            if len(rule) > 1:
                head = rule[0].strip()
                body = rule[1].strip()[:-1]
                bodyAtoms += [item.replace("cx(", "").replace(")", "").replace("-", "").strip()
                              for item in body.split(",")]
                if head == "U":
                    factsFile.write(f'\n{weak_constrint(body, counter)}')
                    counter += 1
                elif head == "F":
                    factsFile.write(f'\n{strong_constrint(body, counter)}')
                    counter += 1
                else:
                    definedAtoms.append(head)
                    trueAndFalseRules += f'{positive_literal(head)} :- {body_rule(body)}'
                    if semantics == "K":
                        trueRulesUnderK += true_rules_under_K(head, body)
                    if head in negatedPartRules.keys():
                        negatedPartRules[head] += "#" + body
                    else:
                        negatedPartRules[head] = body
            else:
                head = rule[0].strip()[:-1]
                definedAtoms.append(head.replace("-", ""))
                trueAndFalseRules += positive_literal(head) + ".\n"

    factsFile.write(f'\n{trueAndFalseRules}')
    factsFile.write(f'\n{negated_part(negatedPartRules)}')
    factsFile.write(f'\n{trueRulesUnderK}')

    if semantics == "K":
        for atom in list(definedAtoms):
            factsFile.write("\n:- not 1  {true(%s); false(%s)}" % (atom, atom))

    if observation:
        factsFile.write(f'\n:- not {positive_literal(observation)}.')
        abducibels = list(set(bodyAtoms) - set(definedAtoms))
        for item in abducibels:
            factsFile.write(f'\natom({item}).')
    elif supported != "Y":
        bodyAtoms = list(set(bodyAtoms))
        for item in bodyAtoms:
            factsFile.write(f'\natom({item}).')

    factsFile.close()
    # print("All atoms: " + str(list(set(bodyAtoms))))
    # print("Def: " + str(list(set(definedAtoms))))
    # print("Diff: " + str(list(set(bodyAtoms) - set(definedAtoms))))
    return writeFilePath, mode


def filename_separator(filePath):
    if filePath.endswith(".lp"):
        return filePath.split(".lp")[0]
    else:
        raise IOError('Please provide an appropriate file. The file should be a .lp file!')


def non_blank_and_non_comment_lines(file):
    for line in file:
        line = line.rstrip()
        if line and not line.startswith("%"):
            yield line


def check_literal(literal):
    if literal.find("-") == -1:
        return "-" + literal.strip()
    else:
        return literal.strip().replace('-', '')


def positive_literal(literal):
    if literal.startswith("-"):
        return f'false({literal[1:]})'
    else:
        return f'true({literal})'


def negative_literal(literal):
    if "cx(" in literal:
        literal = literal.replace("cx(", "").replace(")", "").strip()
        return f'not {positive_literal(literal)}'
    else:
        if literal.startswith("-"):
            return f'true({literal[1:]})'
        else:
            return f'false({literal})'


def body_rule(body):
    bodyToReturn = ""
    literals = body.split(",")
    counter = 1
    size = len(literals)
    for literal in literals:
        if literal:
            literal = literal.replace("cx(", "").replace(")", "").strip()
            if literal.strip().startswith("-"):
                bodyToReturn += f'{positive_literal(literal.strip())}{"." if counter == size else ","}'
            else:
                bodyToReturn += f'{positive_literal(literal.strip())}{"." if counter == size else ","}'
            counter += 1
    return f'{bodyToReturn}\n'


def body_fact(counter, body):
    stringToReturn = ""
    literals = body.split(",")
    for literal in literals:
        if literal:
            literal = literal.replace("cx(", "").replace(")", "").strip()
            if literal.startswith("-"):
                stringToReturn += f'body_neg({counter}, {literal.strip()[1:]}).\n'
            else:
                stringToReturn += f'body_pos({counter}, {literal.strip()}).\n'
    return f'{stringToReturn}'


def negated_part(negatedDictionary):
    stringToReturn = ""
    for key, value in negatedDictionary.items():
        literals = []
        bodies = value.split("#")
        for body in bodies:
            literals.append(body.split(","))
        if len(literals) == 1:
            for item in literals[0]:
                stringToReturn += f'{negative_literal(key.strip())}' \
                                  f' :- {negative_literal(item.strip())}.\n'
        else:
            permutation = list(itertools.product(*literals))
            for item in permutation:
                stringToReturn += f'{negative_literal(key.strip())} :- ' \
                                  f'{",".join([negative_literal(literal.strip()) for literal in item])}.\n'
    return stringToReturn


def true_rules_under_K(head, body):
    stringToReturn = ""
    literals = body.split(",")
    for literal in literals:
        if literal:
            literal = literal.replace("cx(", "").replace(")", "").strip()
            stringToReturn += f'{positive_literal(literal)} :-  {positive_literal(head)}.\n'
    return f'{stringToReturn}'


def weak_constrint(body, counter):
    stringToReturn = ""
    literals = body.split(",")
    for literal in literals:
        if literal:
            if literals.index(literal) != 0:
                stringToReturn += ","
            literal = literal.replace("cx(", "").replace(")", "").strip()
            stringToReturn += f'{positive_literal(literal)}'
    return f'weak(r{counter}) :- {stringToReturn}.\n' \
           f':- weak(r{counter})\n'


def strong_constrint(body, counter):
    stringToReturn = ""
    literals = body.split(",")
    for literal in literals:
        if literal:
            literal = literal.replace("cx(", "").replace(")", "").strip()
            stringToReturn += f'strong(r{counter}) :- {negative_literal(literal)}.\n'
    return f'{stringToReturn}\n' \
           f':- not strong(r{counter})\n'


def execution_mode(observation, supported):
    if observation:
        return 3
    elif supported == "Y":
        return 1
    else:
        return 2

import argparse
from Helper.Parser import *
from Helper.FileHelper import *
from Helper.ClingoHelper import *
from Helper.ReasoningHelper import ReasoningHelper


if __name__ == '__main__':

    argParser = argparse.ArgumentParser()

    argParser.add_argument("-f", "--file", default='',
                           help="The logic program file which we want to encode")
    argParser.add_argument("-o", "--observation", default='',
                           help="The observation that we want to explain")
    argParser.add_argument("-p", "--supported", default='Y',
                           help="Do we want to compute all the minimal models or only the supported models under L and "
                                " S semantics. Y for yes and N for no. Default is Y.")
    argParser.add_argument("-s", "--semantics", default='LS',
                           help="Under which semantics to find the minimal models,  LS - for Łukasiewicz and Gottwald"
                                " S3 semantics or K - for Kleene semantics")
    argParser.add_argument("-r", "--reasonLiteral", type=str, default='',
                           help="The literal that we want to reason with respect to the explanation of the given"
                                "observation.")

    args = argParser.parse_args()
    filePath = args.file
    observation = args.observation
    supported = args.supported
    semantics = args.semantics
    reasonLiteral = args.reasonLiteral

    check_if_file_exists(filePath)
    lpFilePath, mode = execute_encoding(filePath, observation, supported, semantics)
    check_if_file_exists(lpFilePath)

    solutionFilePath = clingo_operation(lpFilePath, mode)
    check_if_file_exists(solutionFilePath)

    if observation != '':
        if reasonLiteral == '':
            print("You didn't provided a  reason literal!")
        else:
            reasoningHelper = ReasoningHelper()
            reasoningHelper.sceptically_reasoning(
                read_solution_with_abducibles(solutionFilePath),
                reasonLiteral)
    else:
        read_solution_without_abducibles(solutionFilePath)

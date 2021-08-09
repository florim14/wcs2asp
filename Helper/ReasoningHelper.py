
class ReasoningHelper:

    @staticmethod
    def sceptically_reasoning(setOfSolution, literal):
        print("\n***********************************************************\n")

        for solution in setOfSolution:
            if literal not in solution:
                print("Reasoning sceptically we cannot conclude: " + literal)
                print("\n***********************************************************\n")
                return

        print("Reasoning sceptically we can conclude: " + literal)
        print("\n***********************************************************\n")

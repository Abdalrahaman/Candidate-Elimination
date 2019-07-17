# sky = ("Sunny", "Rainy", "Cloudy")
# temp = ("Warm", "Cold")
# humdity = ("Normal", "High")
# wind = ("Strong", "Weak")
# water = ("Warm", "Cool")
# forecast = ("Same", "Change")
# enjoy = ("+", "-")

attributesName = (
    ("Sunny", "Rainy", "Cloudy"),
    ("Warm", "Cold"),
    ("Normal", "High"),
    ("Strong", "Weak"),
    ("Warm", "Cool"),
    ("Same", "Change"),
    ("+", "-")
)

specificHypo = [[None, None, None, None, None, None]]

generalHypo = [["?", "?", "?", "?", "?", "?"]]

instances = [
    [attributesName[0][0], attributesName[1][0], attributesName[2][0], attributesName[3][0], attributesName[4][0],
     attributesName[5][0], attributesName[6][0]],

    [attributesName[0][0], attributesName[1][0], attributesName[2][1], attributesName[3][0], attributesName[4][0],
     attributesName[5][0], attributesName[6][0]],

    [attributesName[0][1], attributesName[1][1], attributesName[2][1], attributesName[3][0], attributesName[4][0],
     attributesName[5][1], attributesName[6][1]],

    [attributesName[0][0], attributesName[1][0], attributesName[2][1], attributesName[3][0], attributesName[4][1],
     attributesName[5][1], attributesName[6][0]],
]


def printAllInstances():
    for r in instances:
        for c in r:
            print(c, end=" ")
        print()


def printHypotheses(hypo, n):
    print("h" + str(n) + " =<", end=" ")
    for r in hypo:
        print(r, end=" ")
    print(">")


def isConsistentOrNot(nHypo, n):
    for h in nHypo:
        if h != "?":
            if h != instances[n][nHypo.index(h)]:
                return False
    return True


def isGeneralGreaterSpecific(nHype):
    for v in nHype:
        if v != "?":
            if v != specificHypo[len(specificHypo) - 1][nHype.index(v)]:
                return False
    return True


# print all instances
printAllInstances()

print("///////////// Hypotheses H ////////////////////")


def compute_FindS_Algorithm(i):
    if i[6] == "+":

        if len(specificHypo) == 1:

            specificHypo.append(instances[0][:len(attributesName) - 1])

        else:
            specificHypo.append(list(map(lambda x: x + "", specificHypo[len(specificHypo) - 1])))
            for attribute in range(6):
                if i[attribute] != specificHypo[len(specificHypo) - 1][attribute]:
                    specificHypo[len(specificHypo) - 1][attribute] = "?"
    else:
        specificHypo.append(list(map(lambda x: x + "", specificHypo[len(specificHypo) - 1])))


def compute_ListThen_Algorithm(i):
    # first hypotheses ho=< don't Care, don't Care, don't Care, don't Care, don't Care, don't Care >
    hypotheses = ["?", "?", "?", "?"]

    count = 0

    if i[len(attributesName) - 1] == "-":
        if len(generalHypo) == 1:
            for attribute in range(len(attributesName) - 1):
                for attributeCase in attributesName[attribute]:
                    if i[attribute] != attributeCase:
                        generalHypo.append(list(map(lambda x: x + "", hypotheses)))
                        generalHypo[count][attribute] = attributeCase
                        # printHypotheses(outputHypo[count], count+1)
                        count += 1
        else:
            # More Than one negative hypotheses
            print("More Than one negative hypotheses")
            inconsIndex = 0
            for nextHypo in range(len(generalHypo)):
                hypotheses = list(map(lambda x: x + "", generalHypo[inconsIndex]))
                inconsIndex = generalHypo.index(hypotheses)
                # print(hypotheses, end=" ")
                # print(inconsIndex)

                if isConsistentOrNot(hypotheses, instances.index(i)):
                    # inconsistent when true
                    del generalHypo[inconsIndex]
                    for attribute in range(len(attributesName) - 1):
                        if hypotheses[attribute] == "?":
                            for attributeCase in attributesName[attribute]:
                                if i[attribute] != attributeCase:
                                    generalHypo.insert(inconsIndex, list(map(lambda x: x + "", hypotheses)))
                                    generalHypo[inconsIndex][attribute] = attributeCase
                                    # printHypotheses(outputHypo, inconsIndex)
                                    inconsIndex += 1

                else:
                    inconsIndex += 1


def compute_Candidate_Algorithm():
    for i in instances:

        if i[6] == "+":
            print("d is a positive !")
            for g in generalHypo:
                # check inconsistent to remove it
                if isConsistentOrNot(g, instances.index(i)):
                    del generalHypo[generalHypo.index(g)]

            # compute find-s
            compute_FindS_Algorithm(i)
            # check G > S
            for h in generalHypo:
                if isGeneralGreaterSpecific(h):
                    print("this hypo is greater than Specific")
                else:
                    del generalHypo[generalHypo.index(h)]
        else:
            print("d is a negative !")
            for s in specificHypo:
                # check inconsistent to remove it
                if isConsistentOrNot(s, instances.index(i)):
                    del specificHypo[specificHypo.index(s)]

            # compute List-Then
            compute_ListThen_Algorithm(i)
            # check G > S
            for h in generalHypo:
                if isGeneralGreaterSpecific(h):
                    print("this hypo is greater than Specific")
                else:
                    del generalHypo[generalHypo.index(h)]


compute_Candidate_Algorithm()

# print all specific hypotheses
for h in specificHypo:
    printHypotheses(h, specificHypo.index(h) + 1)

print()

# print all general hypotheses
for h in generalHypo:
    printHypotheses(h, generalHypo.index(h) + 1)

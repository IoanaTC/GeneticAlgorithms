import random
import sys
sys.path.insert(0, 'src')

import codificare, selectie, incrucisare, mutatie

def generateInitialSample(population, a, b):
    sample = []
    for _ in range(population):
        sample.append(random.uniform(a, b))

    return sample
def generateIndividualProbability(population):
    individualProbability = []

    for _ in range(population):
        individualProbability.append(random.uniform(0, 1))

    return individualProbability
    
def getBinaryList(initialSample, a, binaryString_length, sizeOfBin):
    binaryRepresentation = []

    for individual in initialSample:
        binaryRepresentation.append(codificare.calculeazaTO(a, binaryString_length, sizeOfBin, individual))

    return binaryRepresentation

def getFitnessValues(coef_a, coef_b, coef_c, initialSample):
    fitnessValues = []

    for individual in initialSample:
        fitnessValues.append(selectie.fitness(individual, coef_a, coef_b, coef_c))

    return fitnessValues

def getSelectionIntervals(fitnessValues):
    # intervalele de probabilitate ca individul xi sa treaca in generatia urmatoare
    fitnessIntervals = [0]
    # suma tuturor valorilor obtinute din aplicarea functieii de fitness asupra fiecarui
    # individ din populatia data
    F = 0

    for i, value in enumerate(fitnessValues):
        F += value

        # pentru a crea un interval am nevoie sa adun constant valorile intalnite pentru a obtine
        # capetele din stanga ale bin-urilor intermediare
        fitnessIntervals.append(value + fitnessIntervals[i])

    # calcularea propriu-zisa a probabilitatilor
    for i, _ in enumerate(fitnessIntervals):
        fitnessIntervals[i] = format(fitnessIntervals[i] / F, '.7f')

    return fitnessIntervals


def main(population = 20, a = -1, b = 2, coef_a=-1, coef_b=1, coef_c=2, precision=6, crossover=0.25, mutation=0.01, epochs=50):
    # Generarea populatiei initiale: unde populatie = nr de indivizi, cuprinsi in intervalul [domeniu_a, domeniu_b]
    initialSample = generateInitialSample(population, a, b)
    # Obtinerea valorilor de fitness pentru fiecare individ
    fitnessValues = getFitnessValues(coef_a, coef_b, coef_c, initialSample)

    newGeneration = {i: (initialSample[i], fitnessValues[i]) for i in range(population)}

    # Timp de un nr de generatii dat de epochs, vom simula evolutia indivizilor generati in initialSample
    for _ in range(1):
        oldGeneration = newGeneration
        # Crearea unei nnoi generatii pornind de la cea precedenta
        newGeneration = []

        # # Codificarea indivizilor idn populatia curenta
        # binaryString_length, sizeOfBin = codificare.codeConditions(a, b, precision)
        # binaryRepresentation = getBinaryList(initialSample, a, binaryString_length, sizeOfBin)

        # criteriul elitist, gasirea individului cu cea mai mare valoare a functiei de fit
        eliteIndividual = max(oldGeneration.items(), key=lambda x : x[1][1])
        newGeneration = {eliteIndividual[0] : eliteIndividual}

        # Stabilirea intervalelor de selectie
        fitnessIntervals = getSelectionIntervals(fitnessValues)
        individualProbability = generateIndividualProbability(population - 1)

        # Realizarea selectiei
        for p in individualProbability:
            probability = float(p)

            left = 0
            right = population - 1

            while left < right:
                mij = left + (right - left) // 2

                if probability > float(fitnessIntervals[mij]):
                    left = mij + 1
                else:
                    right = mij - 1
            
            newGeneration[left] = oldGeneration[left]

        # Generarea unor noi probabilitati pentru a testa daca un individ este apt pentru any crossover sau mutation
        individualProbability = generateIndividualProbability(population - 1)

        x1, x2 = None, None
        for index, p in enumerate(individualProbability):
            probability = float(p)

            if x1 is not None and x2 is not None:
                punct_rupere = random.randint(0, binaryString_length)

                newGeneration.remove(x1)
                newGeneration.remove(x2)
                cromozom_nou1, cromozom_nou2 = incrucisare.crossover(x1, x2, int(punct_rupere))
                newGeneration.append(cromozom_nou1, cromozom_nou2)
                
                x1 = None
                x2 = None
                continue

            if probability < crossover:
                if x1 is None:
                    x1 = newGeneration[index]
                else:
                    x2 = newGeneration[index]

        print(newGeneration)
main()
import random
from math import ceil, log2, floor


# fucntia de fitness data
def fitness(x, a, b, c):
    return a * (x ** 2) + b * x + c

def generateInitialSample(population, a, b):
    sample = []
    for _ in range(population):
        sample.append(float(random.uniform(a, b)))

    return sample
def generateIndividualProbability(population):
    individualProbability = []

    for _ in range(population):
        individualProbability.append(float(random.uniform(0, 1)))

    return individualProbability

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
        fitnessIntervals[i] = float(format(fitnessIntervals[i] / F, '.7f'))

    return fitnessIntervals

def calculeazaTO(a, l, d, value):
    # pentru value - nr real, trebuie gasit index-ul bin-ului de lungime d
    # cuprins in intervalul [a, b], in care acesta se afla
    # si transformat in sir binar

    # formatare rezultat: sir binar de lungime l
    result = floor((value - a) / d)
    return bin(result)[2:].zfill(l)

def calculeazaFROM(a, l, d, value):
    value = int(value, 2)

    return float(format(a + value * d, f'.{l}f'))

def codeConditions(a, b, p):
    # trebuie sa stabilim param de discretizare
    # l = nr de biti folositi pentru a reprezenta numerele
    l = ceil(log2((b - a)*(10**p)))

    # d pasul de discretizare pentru intervalul [a, b]
    d = (b - a)/(2**l)

    return l, d

def crossover(cromozom1, cromozom2, punctRupere):
    result1 = cromozom1[:punctRupere] + cromozom2[punctRupere:]
    result2 = cromozom2[:punctRupere] + cromozom1[punctRupere:]

    return result1, result2

def main(population = 50, a = -1, b = 2, coef_a=-1, coef_b=1, coef_c=2, precision=6, crossoverProbability=0.25, mutationProbability=0.01, epochs=10):
    def executeCrossover(element1, element2):
        punctRupere = random.randint(0, binaryStringlength - 1)

        candidate1, candidate2 = newGeneration[element1][2], newGeneration[element2][2]
        result1, result2 = crossover(candidate1, candidate2, punctRupere)

        # actualizare date generatie
        result1 = (calculeazaFROM(a, binaryStringlength, sizeOfBin, result1),
                                    fitness(newGeneration[element1][0], coef_a, coef_b, coef_c),
                                    result1)
        result2 = (calculeazaFROM(a, binaryStringlength, sizeOfBin, result2),
                                    fitness(newGeneration[element2][0], coef_a, coef_b, coef_c),
                                    result2)
        
        return result1, result2
    def executeMutation(element):
        string = newGeneration[element][2]
        pozitie = int(random.randint(0, binaryStringlength - 1))

        result = string[:pozitie] + str(1 - int(string[pozitie])) + string[pozitie + 1:]
        return (calculeazaFROM(a, binaryStringlength, sizeOfBin, result),
                                    fitness(newGeneration[element][0], coef_a, coef_b, coef_c),
                                    result)
    
    def executeSelection(probability):
        # Gasim bin-ul in care se incadreaza probabilitatea si 
        # trecem idndividul corespunzator in generatia urmatoare
        left = 0
        right = population

        while left < right:
            mij = left + (right - left) // 2

            if probability > fitnessIntervals[mij]:
                left = mij + 1
            else:
                right = mij - 1

        return left
        
    # lungimea unui binary string si dimenasiunea bin-urilor in care impartim intervalul, in fucntie de a,b,precision
    binaryStringlength, sizeOfBin = codeConditions(a, b, precision)

    # Generarea populatiei initiale: unde populatie = nr de indivizi, cuprinsi in intervalul [domeniu_a, domeniu_b]
    initialSample = generateInitialSample(population, a, b)
    newGeneration = {i: (initialSample[i], fitness(initialSample[i], coef_a, coef_b, coef_c), 
                         calculeazaTO(a, binaryStringlength, sizeOfBin, initialSample[i])) for i in range(population)}

    
    # Timp de un nr de generatii dat de epochs, vom simula evolutia indivizilor generati in initialSample
    for _ in range(epochs):
        oldGeneration = newGeneration
        # Crearea unei noi generatii pornind de la cea precedenta
        newGeneration = {}

        # criteriul elitist, gasirea individului cu cea mai mare valoare a functiei de fit
        individualIndex = 0
        eliteIndividual = max(oldGeneration.items(), key=lambda x : x[1][1])
        newGeneration[individualIndex] =  eliteIndividual[1]
        # Am trecut automat individul cu functia de fit cea mai mare in generatia urmatoare
        # pentru a asigura cel putin egalitatea intre generatii
        population -= 1

        # Stabilirea intervalelor de selectie
        fitnessIntervals = getSelectionIntervals([fitness[1] for fitness in oldGeneration.values()])
        # Realizarea selectiei
        # generarea unui nr de probabilitati de selectie = populatia fara individul elitist
        individualProbability = generateIndividualProbability(population)

        for probability in individualProbability:
            individualIndex += 1
            selectedIndividual = executeSelection(probability)
            newGeneration[individualIndex] = oldGeneration[selectedIndividual]
        
        # Generarea unor noi probabilitati pentru a testa daca un individ este apt pentru any crossover sau mutation
        crossoverToBe = []
        individualProbability = generateIndividualProbability(len(newGeneration))

        for index, candidate in enumerate(newGeneration):
            if individualProbability[index] <= crossoverProbability:
                crossoverToBe.append(candidate)

        if len(crossoverToBe) > 1:
            # Realizarea incrucisarii intre membrii selectati
            noCandidates = len(crossoverToBe)
            lastCandidate = -1

            if noCandidates % 3 == 1:
                lastCandidate = -3
                element1, element2 = crossoverToBe[lastCandidate], crossoverToBe[lastCandidate + 1]
                # actualizare date generatie
                newGeneration[element1], newGeneration[element2] = executeCrossover(element1, element2)
                
                element1, element2 = crossoverToBe[lastCandidate + 1], crossoverToBe[lastCandidate + 2]
                # actualizare date generatie
                newGeneration[element1], newGeneration[element2] = executeCrossover(element1, element2)

            for element1, element2 in zip(crossoverToBe[:lastCandidate:2], crossoverToBe[1:lastCandidate:2]):
                newGeneration[element1], newGeneration[element2] = executeCrossover(element1, element2)
        
        mutationToBe = []
        individualProbability = generateIndividualProbability(len(newGeneration))

        for index, candidate in enumerate(newGeneration):
            if individualProbability[index] <= mutationProbability:
                newGeneration[candidate] = executeMutation(candidate)
        
        population += 1
        print(len(newGeneration), max(newGeneration.items(), key=lambda x:x[1][1]))

if __name__ == "__main__":
    main()
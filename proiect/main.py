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

# def crossover2(cromozom1, cromozom2, punctRupere1, punctRupere2):
#     result1 = cromozom1[:punctRupere1] + cromozom2[punctRupere1:punctRupere2] + cromozom1[punctRupere2:]
#     result2 = cromozom2[:punctRupere1] + cromozom1[punctRupere1:punctRupere2] + cromozom2[punctRupere2:]

def main(population, a, b, coef_a, coef_b, coef_c, precision, crossoverProbability, mutationProbability, epochs):
    file_path = "Evolutie.txt"
    f = open(file_path, "w")

    f.write(file_path)
    f.write("\n\nPopulatia initiala:\n")

    maximum = []

    def executeCrossover(element1, element2):
        punctRupere = random.randint(0, binaryStringlength - 1)

        candidate1, candidate2 = newGeneration[element1][2], newGeneration[element2][2]
        result1, result2 = crossover(candidate1, candidate2, punctRupere)

        if ok == 0:
            f.write(f"\nRecombinare intre cromozomul {element1} cu {element2}\n")
            f.write(f"{candidate1}        {candidate2}  punct {punctRupere}\n")
            f.write(f"Rezultat:  {result1}        {result2}\n")

        # actualizare date generatie
        result1 = (calculeazaFROM(a, binaryStringlength, sizeOfBin, result1),
                                    fitness(newGeneration[element1][0], coef_a, coef_b, coef_c),
                                    result1)
        result2 = (calculeazaFROM(a, binaryStringlength, sizeOfBin, result2),
                                    fitness(newGeneration[element2][0], coef_a, coef_b, coef_c),
                                    result2)
        
        return result1, result2
    
    def executeMutation(element):
        modified = False
        string = newGeneration[element][2]

        result = string
        for pozitie, gene in enumerate(list(string)):
            probability = random.uniform(0, 1)
            if probability <= mutationProbability:
                result = result[:pozitie] + str(1 - int(result[pozitie])) + result[pozitie + 1:]
                modified = True
                
        newValue = calculeazaFROM(a, binaryStringlength, sizeOfBin, result)
        return (newValue, fitness(newValue, coef_a, coef_b, coef_c), result), modified
    
    def executeSelection(probability):
        # Gasim bin-ul in care se incadreaza probabilitatea si 
        # trecem idndividul corespunzator in generatia urmatoare
        left = 0
        right = population - 1

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

    for index, individual in enumerate(newGeneration.values()):
        f.write(f"      {index}: {individual[2]} x = {individual[0]} f = {individual[1]}\n")

    f.write("\nPobabilitati selectie:\n")

    # Timp de un nr de generatii dat de epochs, vom simula evolutia indivizilor generati in initialSample
    for ok in range(epochs):
        oldGeneration = newGeneration
        # Crearea unei noi generatii pornind de la cea precedenta
        newGeneration = {}
        individualIndex = 0
        # Am trecut automat individul cu functia de fit cea mai mare in generatia urmatoare
        # pentru a asigura cel putin egalitatea intre generatii
        # population -= 1

        # Stabilirea intervalelor de selectie
        fitnessIntervals = getSelectionIntervals([fitness[1] for fitness in oldGeneration.values()])
        # Realizarea selectiei
        # generarea unui nr de probabilitati de selectie = populatia fara individul elitist
        individualProbability = generateIndividualProbability(population)

        if ok == 0:
            for  index, interval in enumerate(fitnessIntervals[1:]):
                f.write(f"cromozom      {index} probabilitate {fitnessIntervals[index + 1] - fitnessIntervals[index]}\n")

            f.write("\nIntervale probabilitati selectie:\n")
            for index, interval in enumerate(fitnessIntervals):
                if index % 10 == 0:
                    f.write("\n")
                f.write(f"{interval}    ")
            f.write("\n\n")

        for probability in individualProbability:
            selectedIndividual = executeSelection(probability)

            if ok == 0:
                f.write(f"u = {probability} selectam cromozomul {selectedIndividual}\n")

            newGeneration[individualIndex] = oldGeneration[selectedIndividual]
            individualIndex += 1
        
        if ok == 0:
            f.write("\n\nDupa selectie:\n")
            for index, individual in enumerate(newGeneration.values()):
                f.write(f"      {index}: {individual[2]} x = {individual[0]} f = {individual[1]}\n")

        # Generarea unor noi probabilitati pentru a testa daca un individ este apt pentru any crossover sau mutation
        crossoverToBe = []
        individualProbability = generateIndividualProbability(len(newGeneration))
        if ok == 0:
            f.write(f"\n\nProbabilitatea de incrucisare {crossoverProbability}: \n")
        for index, candidate in enumerate(newGeneration):
            if ok == 0:
                f.write(f"      {index}: {newGeneration[candidate][2]} u = {individualProbability[index]}")
            if individualProbability[index] <= crossoverProbability:
                if ok == 0:
                    f.write(f" < {crossoverProbability}  participa")
                crossoverToBe.append(candidate)
            if ok == 0:
                f.write("\n")
        
        if len(crossoverToBe) > 1:
            # Realizarea incrucisarii intre membrii selectati
            noCandidates = len(crossoverToBe)
            lastCandidate = -1

            if noCandidates % 2 == 1:
                lastCandidate = -3
                element1, element2 = crossoverToBe[lastCandidate], crossoverToBe[lastCandidate + 1]
                # actualizare date generatie
                newGeneration[element1], newGeneration[element2] = executeCrossover(element1, element2)
                
                element1, element2 = crossoverToBe[lastCandidate + 2], crossoverToBe[0]
                # actualizare date generatie
                newGeneration[element1], newGeneration[element2] = executeCrossover(element1, element2)

            crossover1, crossover2 = crossoverToBe[:lastCandidate:2], crossoverToBe[1::2]

            for element1, element2 in zip(crossover1, crossover2):
                newGeneration[element1], newGeneration[element2] = executeCrossover(element1, element2)
        elif len(crossoverToBe) == 1:
            if ok == 0:
                f.write("Recombinarea cu el insusi denota acelasi rezultat\n")
        else:
            if ok == 0:
                f.write("Nu au fost selectate elemente pentru incrucisare\n")

        if ok == 0:
            f.write("\n\nDupa recombinare:\n")
            for index, individual in enumerate(newGeneration.values()):
                f.write(f"      {index}: {individual[2]} x = {individual[0]} f = {individual[1]}\n")
            
            f.write(f"\n\nProbabilitate de mutatie pentru fiecare gena {mutationProbability}\n")
            f.write("Au fost modificati cromozomii:\n")
            
        mutationToBe = []
        # individualProbability = generateIndividualProbability(len(newGeneration))

        for index, candidate in enumerate(newGeneration):
            print(newGeneration[candidate])
            newGeneration[candidate], modified = executeMutation(candidate)
            print(newGeneration[candidate], "after")
            if modified == True:
                mutationToBe.append(candidate)
        
        if ok == 0:
            for i in range(len(mutationToBe)):
                f.write(f"{mutationToBe[i]}\n")

            f.write("\nDupa mutatie: \n")
            for index, individual in enumerate(newGeneration.values()):
                f.write(f"      {index}: {individual[2]} x = {individual[0]} f = {individual[1]}\n")

            f.write("\nEvolutia maximului: \n")

        # population += 1
        # criteriul elitist, gasirea individului cu cea mai mare valoare a functiei de fit
        eliteIndividual = max(oldGeneration.items(), key=lambda x : x[1][1])
        
        newGeneration[population] =  eliteIndividual[1]
        currentMaximum = max(newGeneration.values(), key=lambda x:x[1])[1]
        maximum.append(currentMaximum)

        f.write(f"{currentMaximum}\n")

    f.close()
    return maximum

if __name__ == "__main__":
    main()
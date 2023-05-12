# fucntia de fitness data
def fitness(x, a, b, c):
    return a * (x ** 2) + b * x + c

def main():
    # a, b, c coeficientii polinomiali ai functiei de fit
    # n dimensiunea populatiei de cromozomi
    # x (0 - n-1) valoarea decodificata a fiecarui cromozom

    a, b, c = [int(x) for x in input().strip().split()]
    n = int(input())

    populatie = [float(x) for x in input().strip().split()]

    # intervalele de probabilitate ca individul xi sa treaca in generatia urmatoare
    fitness_intervals = [0]
    # suma tuturor valorilor obtinute din aplicarea functieii de fitness asupra fiecarui
    # individ din populatia data
    F = 0

    for i, x in enumerate(populatie):
        value = fitness(x, a, b, c)
        F += value

        # pentru a crea un interval am nevoie sa adun constant valorile intalnite pentru a obtine
        # capetele din stanga ale bin-urilor intermediare
        fitness_intervals.append(value + fitness_intervals[i])

    # calcularea propriu-zisa a probabilitatilor
    for i, _ in enumerate(fitness_intervals):
        fitness_intervals[i] /= F

    for value in fitness_intervals:
        print(float(format(value, '.7f')))
    
if __name__ == "__main__":
    main()
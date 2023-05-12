# functia de crossover
def crossover(cromozom1, cromozom2, punctRupere):
    result1 = cromozom1[:punctRupere] + cromozom2[punctRupere:]
    result2 = cromozom2[:punctRupere] + cromozom1[punctRupere:]

    return result1, result2

def main():
    # l = lungimea cromozomilor cu care lucram
    # x1, x2 = cromozomii in cauza
    # i = punctul de rupere folosit in efectuarea incrucisarii

    l = int(input())
    x1, x2 = [input() for _ in range(2)]
    i = int(input())

    x1, x2 = crossover(x1, x2, i)
    print(x1, x2, sep = "\n")

if __name__ == "__main__":
    main()
from math import ceil, log2, floor
    
def calculeazaTO(a, l, d, value):
    # pentru value - nr real, trebuie gasit index-ul bin-ului de lungime d
    # cuprins in intervalul [a, b], in care acesta se afla
    # si transformat in sir binar
    index = None
    no_of_bins = 2**l

    # cautare binara a capatului din stanga al fiecarui bin, avand pasul d 
    left = a
    right = a + (no_of_bins - 1) * d

    while left < right:
        mij = left + ((right - a) - (left - a)) / 2

        if value > mij:
            left = mij + d
            index = (left - a) / d
        else:
            right = mij - d

    # formatare rezultat: sir binar de lungime l
    result = floor(index)
    return bin(result)[2:].zfill(l)

def calculeazaFROM(a, l, d, value):
    value = int(value, 2)

    return float(format(a + value * d, f'.{l}f'))

def main():
    result = []

    # Se citesc de la tastatura capetele intrvalului [a, b]
    # Precizia de discretizare p (nr natural)
    # m teste TO, FROM

    a, b = [int(x) for x in input().strip().split()]
    p = int(input())
    m = int(input())

    # trebuie sa stabilim param de discretizare
    # l = nr de biti folositi pentru a reprezenta numerele
    l = ceil(log2((b - a)*(10**p)))

    # d pasul de discretizare pentru intervalul [a, b]
    d = (b - a)/(2**l)

    for _ in range(m):
        message = input()
        
        if message == "TO":
            # se da un nr real x, se cere un sir binar
            value = float(input())
            result.append(calculeazaTO(a, l, d, value))

        elif message == "FROM":
            # se da un sir binar, se cere un nr real
            value = input()
            result.append(calculeazaFROM(a, l, d, value))
        else:
            return
        
    for element in result:
        print(element)


if __name__ == "__main__":
    main()
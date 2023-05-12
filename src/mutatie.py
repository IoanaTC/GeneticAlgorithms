def main():
    # l = lungimea cromozomilor
    # k = nr de mutatii pe care le vom aplica pe genotipul unui cromozom
    # C = cromozomul care va suferi mutatiile
    # o lista cu k indici care vor reprezenta pozitiile genelor carora li se va aplica un flip

    l, k = [int(x) for x in input().strip().split()]
    C = []
    C[:0] = input()
    lista_indici = [int(i) for i in input().strip().split()]

    # mutatiile propriu-zise, 1 devine 0 si viceversa
    for i in lista_indici:
        C[i] = str(1 - int(C[i]))

    C = "".join(C)
    print(C)

if __name__ == "__main__":
    main()
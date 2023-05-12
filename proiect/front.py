from tkinter import *
from main import main

master = Tk()
master.title("GA")
master.geometry("800x250")

def get_values():
    populatie = int(dimensiuneaPopulatiei.get())

    domeniu_a = float(domeniuDefinitie_stanga.get())
    domeniu_b = float(domeniuDefinitie_dreapta.get())

    a = float(coeficientiiPolinom_a.get())
    b = float(coeficientiiPolinom_b.get())
    c = float(coeficientiiPolinom_c.get())

    precizie = float(precizieDiscretizare.get())
    crossover = float(crossoverPropbabilitate.get())
    mutatie = float(mutatieProbabilitate.get())
    generatii = int(etape.get())

    main(populatie, domeniu_a, domeniu_b, a, b, c, precizie, crossover, mutatie, generatii)


Label(master, text='Algoritmi Genetici', font=20).grid(row=0)

Label(master, text='Dimensiunea populatiei').grid(row=1)
Label(master, text='Domeniul de definitie al functiei').grid(row=6)
Label(master, text='Coeficientii functiei de fitness').grid(row=7)
Label(master, text='Precizia manipularii datelor').grid(row=2)
Label(master, text='Probabilitatea de crossover').grid(row=3)
Label(master, text='Probabilitatea de mutatie').grid(row=4)
Label(master, text='Numarul de etape ale algoritmului').grid(row=5)

dimensiuneaPopulatiei = Entry(master)
dimensiuneaPopulatiei.grid(row=1, column=1)

Label(master, text='a = ').grid(row=6, column=1)
domeniuDefinitie_stanga = Entry(master)
domeniuDefinitie_stanga.grid(row=6, column=2)
Label(master, text='b = ').grid(row=6, column=3)
domeniuDefinitie_dreapta = Entry(master)
domeniuDefinitie_dreapta.grid(row=6, column=4)

Label(master, text='a = ').grid(row=7, column=1)
coeficientiiPolinom_a = Entry(master)
coeficientiiPolinom_a.grid(row=7, column=2)
Label(master, text='b = ').grid(row=7, column=3)
coeficientiiPolinom_b = Entry(master)
coeficientiiPolinom_b.grid(row=7, column=4)
Label(master, text='c = ').grid(row=7, column=5)
coeficientiiPolinom_c = Entry(master)
coeficientiiPolinom_c.grid(row=7, column=6)

precizieDiscretizare = Entry(master)
precizieDiscretizare.grid(row=2, column=1)
crossoverPropbabilitate = Entry(master)
crossoverPropbabilitate.grid(row=3, column=1)
mutatieProbabilitate = Entry(master)
mutatieProbabilitate.grid(row=4, column=1)
etape = Entry(master)
etape.grid(row=5, column=1)

Button(master, text="Generate response", command=get_values).grid(row=8)

master.mainloop()

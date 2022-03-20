import clases

columnas = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8}

celdas = list()

for x in range(8):
    for y in range(8):
        celdas += Descriptor([columnas[x], y])
        
posibles = celdas
from functions import *
from clases import *

d = Damas()

 


r1 = open('regla1.txt','r')
regla1 = r1.read()
r1.close()

r2 = open('regla2.txt','r')
regla2 = r2.read()
r2.close()

r3 = open('regla3.txt','r')
regla3 = r3.read()
r3.close()

r4 = open('regla4.txt','r')
regla4 = r4.read()
r4.close()




A = Ytoria([ regla4, regla1, regla2, regla3])

S, I = SATsolver(A)
if I != None:
    d.visualizar(I)
else:
    print('¡No hay solución!')

d.visualizar(I)


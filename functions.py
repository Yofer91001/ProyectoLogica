import declarations 


def setDiagonalsConstraint(c, r):
    constraints = list
    
    for i in celdas:
        if (r - visualizar_formula(i, Descriptor)[1]) == (columnas[c] - visualizar_formula(i, Descriptor)[0]):
            posibles -= i
            constraints +=  i
            
    return constraints
                    

def setColumnConstraint(c, r):
    
    constraints = list
    
    for i in celdas:
        if r != visualizar_formula(i, Descriptor)[1] and c == visualizar_formula(i, Descriptor)[0]:
            posibles -= i
            constraints +=  i
            
    return constraints
                    
                

def setRowConstraint(x):
    constraints = list
    
    for i in celdas:
        if c != visualizar_formula(i, Descriptor)[0] and r == visualizar_formula(i, Descriptor)[1]:
            posibles -= i
            constraints +=  i
            
    return constraints
   


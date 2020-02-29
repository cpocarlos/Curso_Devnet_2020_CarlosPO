#!/usr/bin/python

# Calculadora (es una tarea a la que le añadiremos más funcionalidades)

#     Crear un menú que indique las opciones que hay
#     Como mínimo, incluir: suma, resta, multiplicación, división, exponenciales y raíces cuadradas. Se pueden añadir más funcionalidades.
#     Podéis usar las funciones y técnicas vistas en las sesiones, o implementar otras que consideréis oportunas. Obviamente, ser eficientes tendrá más nota.


# Importamos librerias que vamos a usar
import math
import sys

# Variables
pantalla = 0    # Valor que mostrara en pantalla
primer = True   # Boolean para saber si es la primera vez que se usa
operacion = ""  # La operacion que quiere realizar el usuario
num2 = 0        # Variable donde almacenar el 2º valor de la operacion

menu = """
Seleccione operacion:
    s - suma
    r - resta
    m - multiplicacion
    d - division
    e - exponencial
    c - raiz cuadrada
    l - limpiar pantalla
    x - salir
>"""

operaciones_posibles = {
    "s":"+",
    "r":"-",
    "m":"*",
    "d":"/",
    "e":"^",
    "c":"√",
    "l":"limpiar",
    "x":"salir"
}

# Funciones
def suma(a, b):
    return(a+b)

def resta(a,b):
    return(a-b)

def multiplicacion(a,b):
    return(a*b)

def division(a,b):
    try:
        return(a/b)
    except:
        print("ERROR: estas haciendo una operacion prohibida")
        return(0)

def exponencial(a):
    try:
        return(math.exp(a))
    except:
        print("ERROR: estas haciendo una operacion prohibida")
        return(0)

def raiz_cuadrada(a):
    try:
        return(math.sqrt(a))
    except:
        print("ERROR: estas haciendo una operacion prohibida")
        return(0)


# Funcion que comprueba si el valor introducido es valido (int/float) y lo devuelve preferiblemente en INT, luego en FLOAT y sino devuelve un False
def verifica_valor(valor):
    #Si es 0 lo devolvemos directamente
    if valor == 0:
        return(int(0))
    else:   #Si no es 0 lo procesamos
        try:
            #Verificamos si se puede convertir a INT
            valor_devolver = int(valor)
            return(valor_devolver)
        except ValueError:
            try:
                valor_devolver = float(valor)
                return(valor_devolver)
            except ValueError:
                print ("ERROR: Por favor introduce un numero!!") 
                return("ERROR")

def solicita_primer_valor():
    #if primer==True:    #Si es la 1ª vez tenemos que pedir los 2 nº
    num1 = verifica_valor(input("Primer valor: "))      #Pedimos el primer nº y miramos si realmente es un nº
    while num1 == "\nERROR":
        num1 = verifica_valor(input("Primer valor: "))
    print(num1,end='')
    primer=False
    return(num1)

def solicita_segundo_valor():
    num2 = verifica_valor(input(operaciones_posibles[operacion]))   #Pedimos el segundo nº y miramos si realmente es un nº
    while num2 == "\nERROR":
        num2 = verifica_valor(input(operaciones_posibles[operacion]))
    return(num2)


# Empieza la ejecución

#Mientras no pulsen X estamos no salimos del programa
while operacion != 'x':
    operacion = input(menu)     #Solicitamos operacion a realizar
    while operacion not in operaciones_posibles:    #Verificamos que realmente nos introducen una operacion valida
        print("INTRODUCE SOLO UNA DE LAS OPERACIONES POSIBLES!!")
        operacion = input(menu)

    #Si pulsaron X es que quieren salir
    if operacion == "x":
        print("Saliendo...")
        sys.exit(0)

    #Si pulsaron L es que quieren limpiar pantalla
    elif operacion == "l":
        pantalla = 0
        primer = True

    #Dependiendo de la operacion elegida llamamos a la funcion necesaria
    elif operacion == "s":
        if primer == True:
            pantalla = suma(solicita_primer_valor(),solicita_segundo_valor())
            primer = False
        else:
            print(pantalla,end='')
            pantalla = suma(pantalla,solicita_segundo_valor())
    
    elif operacion == "r":
        if primer == True:
            pantalla = resta(solicita_primer_valor(),solicita_segundo_valor())
            primer = False
        else:
            print(pantalla,end='')
            pantalla = resta(pantalla,solicita_segundo_valor())

    elif operacion == "m":
        if primer == True:
            pantalla = multiplicacion(solicita_primer_valor(),solicita_segundo_valor())
            primer = False
        else:
            print(pantalla,end='')
            pantalla = multiplicacion(pantalla,solicita_segundo_valor())

    elif operacion == "d":
        if primer == True:
            pantalla = division(solicita_primer_valor(),solicita_segundo_valor())
            primer = False
        else:
            print(pantalla,end='')
            pantalla = division(pantalla,solicita_segundo_valor())

    elif operacion == "e":
        if primer == True:
            pantalla = exponencial(solicita_segundo_valor())
            primer = False
        else:
            print("^"+str(pantalla),end='')
            pantalla = exponencial(pantalla)

    elif operacion == "c":
        if primer == True:
            pantalla = raiz_cuadrada(solicita_segundo_valor())
            primer = False
        else:
            print("^"+str(pantalla),end='')
            pantalla = raiz_cuadrada(pantalla)


        
    #Imprimimos resultado por pantalla
    print("\n\tRESULTADO->",pantalla)



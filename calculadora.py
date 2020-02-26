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



# Empieza la ejecución
while operacion != 'x':
    operacion = input(menu)
    while operacion not in operaciones_posibles:
        print("INTRODUCE SOLO UNA DE LAS OPERACIONES POSIBLES!!")
        operacion = input(menu)

    if operacion == "x":
        print("Saliendo...")
        sys.exit(0)
    elif operacion == "l":
        pantalla = 0
        primer = True

    else:   #Si realmente es una operacion lo que vamos a realizar
        if primer==True:    #Si es la 1ª vez tenemos que pedir los 2 nº
            pantalla = verifica_valor(input("Primer valor: "))      #Pedimos el primer nº y miramos si realmente es un nº
            while pantalla == "ERROR":
                pantalla = verifica_valor(input("Primer valor: "))

            num2 = verifica_valor(input(str(pantalla) + operaciones_posibles[operacion]))   #Pedimos el segundo nº y miramos si realmente es un nº
            while num2 == "ERROR":
                num2 = verifica_valor(input(str(pantalla) + operaciones_posibles[operacion]))
            primer = False
        else:               #Si ya tenemos algo en pantalla solo necesitamos el 2º nº
            num2 = verifica_valor(input(str(pantalla) + operaciones_posibles[operacion]))

        #Dependiendo de la operacion elegida llamamos a la funcion necesaria
        if operacion == "s":
            pantalla = suma(pantalla,num2)
        elif operacion == "r":
            pantalla = resta(pantalla,num2)
        elif operacion == "m":
            pantalla = multiplicacion(pantalla,num2)
        elif operacion == "d":
            pantalla = division(pantalla,num2)

        
    #Imprimimos resultado por pantalla
    print("RESULTADO->",pantalla)



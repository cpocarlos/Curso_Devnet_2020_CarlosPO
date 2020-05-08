#!/usr/bin/env python3

# Crear un programa que permita conectarse con el controlador APIC-EM de Cisco

#     El usuario tendrá que escoger la opción que quiera (no tendrá que especificar la url a mano)
#     Añadir, como mínimo, 4 funcionalidades

# OPCIONES
# 1 - Imprimir Host por pantalla
# 2 - Exportar Host a CSV
# 3 - Mostrar detalles de Host (por MAC)
# 4 - 
# 5 - Salir
###################################################################################################

# Importamos librerias necesarias
import json
import sys
import csv
import os
import time
import pprint
try:
    import requests
except:
    print("ERROR: no se ha podido encontrar la libreria Requests. Revisa que la tengas instalada")
    sys.exit()
try:
    import urllib3
except:
    print("ERROR: no se ha podido encontrar la libreria Urllib3. Revisa que la tengas instalada")
    sys.exit()
try:
    from tabulate import tabulate
except:
    print("ERROR: no se ha podido encontrar la libreria Tabulate. Revisa que la tengas instalada")
    sys.exit()



# Definimos variables
server = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/"
headers = {
    'Content-Type':'application/json'
}
body_json ={
    "password": "Xj3BDqbU",
    "username": "devnetuser"
}
ticket = ""  #Definimos el ticket vacio

menu = {
    "1":"Inventario: Listar Host por pantalla",
    "2":"Inventario: Exportar Host a CSV",
    "3":"Inventario: Mostrar detalles de Host (ID) por pantalla",
    "4":"No hace nada",
    "5":"Salir"
}

bucle_activo = True


# Definimos primero las funciones
requests.packages.urllib3.disable_warnings()

#Funcion para crear el ticket, luego devuelve el ticket generado
def crea_ticket():
    print("Autenticando...")
    resp = requests.post(server+'ticket',json.dumps(body_json),headers=headers,verify=False)    
    #print(resp.status_code)

    # Verificamos que tengamos una respuesta satisfactoria
    if resp.status_code == 200:
        respuesta_json = resp.json()
        #print("Respuesta Json: ", respuesta_json)
        #print("Ticket: ", respuesta_json['response']['serviceTicket'])
        print("Autenticacion correcta")        
        ticket = respuesta_json['response']['serviceTicket']
        headers["X-Auth-Token"] = ticket
        return(respuesta_json['response']['serviceTicket'])

    else:
        print("ERROR: algo fallo al solicitar el ticket")
        sys.exit(1)

# Funcion que devuelve lista de host
def lista_host():
    global ticket
    
    #Verificamos si tenemos un ticket activo. Sino lo creamos
    if ticket == '':
        ticket = crea_ticket()        

    #Si ya teniamos ticket seguimos
    resp = requests.get(server+'host',headers=headers,verify=False)    
    #print(resp.status_code)

    # Verificamos que tengamos una respuesta satisfactoria
    if resp.status_code == 200:
        respuesta_json = resp.json()
        #print("Respuesta Json: ", respuesta_json)
        return(respuesta_json['response'])

    else:
        print("ERROR: algo fallo al solicitar el host")
        sys.exit(1)

# Funcion que devuelve detalles de un host
def detalles_host(identificador):
    global ticket
    
    #Verificamos si tenemos un ticket activo. Sino lo creamos
    if ticket == '':
        ticket = crea_ticket()        

    #Si ya teniamos ticket seguimos
    resp = requests.get(server+'host/'+identificador,headers=headers,verify=False)    
    #print(resp.status_code)
    respuesta_json = resp.json()

    # Verificamos que tengamos una respuesta satisfactoria
    if resp.status_code == 200:        
        #print("Respuesta Json: ", respuesta_json)
        return(respuesta_json['response'])

    else:
        try:
            print("ERROR: algo fallo al solicitar el host.\n", respuesta_json['response']['message'])
        except:
            print("ERROR: algo fallo al solicitar el host")
        


# Empieza la ejecucion general
def main():
    global menu
    opcion_elegida = ""

    # Mostramos el Menú y solicitamos la opción deseada. Verificamos que realmente es una opción posible
    while opcion_elegida != '5' and opcion_elegida not in menu:
        print("\n\t-----> MENU PRINCIPAL <-----")
        for entrada in menu:
            print(entrada + ' - ' + menu[entrada])
        opcion_elegida = input("> ")

    # Si eligieron listar host por pantalla
    if opcion_elegida == '1':
        listado_personalizado = []

        #Obtenemos el listado total de Hosts de APIC-EM
        listado_total = lista_host()

        #Creamos una vista personalizada recorriendo los host y quedandonos con los campos que nos interesan
        for host in listado_total:
            try:
                listado_personalizado.append([host['id'],host['hostIp'],host['hostMac'],host['hostType']])
            except:
                print("ERROR: Hubo algun problema recopilando datos del host ", host)

        #Imprimimos por pantalla el listado personalizado
        print(tabulate(listado_personalizado, headers=["ID","IP", "MAC", "Tipo"]))

    # Si eligieron exportar el listado de host a CSV
    elif opcion_elegida == '2':
        listado_personalizado = []
        path = os.path.dirname(os.path.abspath(__file__))        
        #print("Este es el PATH: ",path)
        f_salida = os.path.join(path,"export_host-"+(time.strftime("%Y%m%d-%H%M%S"))+".csv")

        #Obtenemos el listado total de Hosts de APIC-EM
        listado_total = lista_host()

        #Cabecera para los datos a exportar
        cabecera = ["ID", "IP", "MAC", "Tipo"]

        #Creamos lista personalizada de lo que queremos exportar
        for host in listado_total:
            try:
                listado_personalizado.append([host['id'],host['hostIp'],host['hostMac'],host['hostType']])
            except:
                print("ERROR: Hubo algun problema recopilando datos del host ", host)

        myFile = open(f_salida, 'w', newline='')
        with myFile:
            writer = csv.writer(myFile)
            writer.writerow(cabecera)
            writer.writerows(listado_personalizado)
            """ for linea in listado_personalizado:
                writer.writerow(linea) """

        print("Exportación realizada en ", f_salida)

    # Si eligieron consultar detalles de Host por ID
    elif opcion_elegida == '3':
        #Pedimos el ID del Host
        identificador_host = input("Introduce el ID del Host a consultar: ")

        #Llamamos a la funcion y le pasamos el ID solicitado
        info = detalles_host(identificador_host)

        #Imprimimos por pantalla los detalles del Host
        pprint.pprint(info)  

    # Opcion salir
    elif opcion_elegida == '5':
        print("Hasta la proxima!")
        sys.exit(0)

        




# Ejecutamos el programa
if __name__== "__main__":
    while True:
        main()


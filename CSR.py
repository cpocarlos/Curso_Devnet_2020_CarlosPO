#!/usr/bin/env python3

#Autor: Carlos Pena Oro

# Crear un script que permita conectarnos a nuestra Router CSR1000v (bien sea en local o a través del Sandbox) y que, a través de un menú, nos aparezcan una serie de opciones que nos permita realizar las siguientes tareas:

#     Obtener un listado de las interfaces del router (indicar, en modo tabla, el nombre de la interfaz, su IP y MAC)
#     Crear Interfaces
#     Borrar Interfaces
#     Obtener la tabla de routing y crear una tabla con Identificador (0,1,2...), Red de destino, e Interfaz de salida.
#     Implementar una petición a 2 módulos de yang diferentes compatibles con nuestro router

###################################################################################################

# Importamos librerias necesarias

# Importamos librerias necesarias
import json
import sys
import csv
import os
import time
import pprint
from ncclient import manager
import xml.dom.minidom
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
try:
    import xmltodict
except:
    print("ERROR: no se ha podido encontrar la libreria xmltodict. Revisa que la tengas instalada")
    sys.exit()



# Definimos variables
deviceIP = "10.10.20.48"
username = "developer"
password = "C1sco12345"

ticket = ""  #Definimos el ticket vacio

menu = {
    "1":"Obtener un listado de las interfaces (RESTCONF)",
    "2":"Crear Interfaces (NETCONF)",
    "3":"Borrar Interfaces (NETCONF)",
    "4":"Obtener la tabla de routing (NETCONF)",
    "5":"Salir"
}

bucle_activo = True


# Definimos primero las funciones
requests.packages.urllib3.disable_warnings()


def obtenInterfaces():
    # Construimos URL
    url1 = "https://"+deviceIP+"/restconf/data/ietf-interfaces:interfaces/"
    url2 = "https://"+deviceIP+"/restconf/data/ietf-interfaces:interfaces-state/interface"

    # Contruimos cabecera
    #headers
    headers={"Accept":"application/yang-data+json","Content-type":"application/yang-data+json"}
    #Authentification
    basic_auth=(username,password)

    # Lanzamos consulta
    resp=requests.get(url1,headers=headers,auth=basic_auth,verify=False)
    resp2=requests.get(url2,headers=headers,auth=basic_auth,verify=False)

    # Verificamos que tengamos una respuesta satisfactoria
    if resp.status_code == 200 and resp2.status_code == 200:
        respuesta_json = resp.json()
        respuesta2_json = resp2.json()
        #pprint.pprint(respuesta_json)

        listaInterfaces = []

        print("Listado de interfaces:")

        # Recorremos cada interfaz
        for interface in respuesta_json["ietf-interfaces:interfaces"]["interface"]:
            # pprint.pprint(interface["name"] + '/t' + interface["ietf-ip:ipv4"]["address"][0]["ip"] + "/t" )
            interfazName = interface["name"]
            try:
                interfazIP = interface["ietf-ip:ipv4"]["address"][0]["ip"]
            except:
                interfazIP = "No tiene IP"
            
            # Recorro el segundo diccionario con interfaces y mac
            for i in respuesta2_json["ietf-interfaces:interface"]:
                if i["name"] == interfazName:
                    interfazMAC = i["phys-address"]
                    break
            detallesinterfaz=[interfazName, interfazIP, interfazMAC]               
            listaInterfaces.append(detallesinterfaz)
            
        # Imprimo los valores de interfaz
        #pprint.pprint("-"+interfazName+'\t'+interfazIP+'\t'+interfazMAC)
        #print(tabulate(listaInterfaces))
        return(listaInterfaces)
    else:
            print("ERROR: algo fallo al solicitar al host")
            sys.exit(1)


def creaInterface():
    # Definimos conexión
    con = manager.connect(host=deviceIP,port=830,username=username,password=password,hostkey_verify=False)

    # Definimos la interface
    plantilla_interface = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{name}</name>
                <description>{desc}</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    ianaift:softwareLoopback
                </type>
                <enabled>{status}</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{ip_address}</ip>
                        <netmask>{mask}</netmask>
                    </address>
                </ipv4>
            </interface>
         </interfaces>
    </config>"""
    # Pedimos los detalles para la interface
    nueva_interface = {}
    nueva_interface["name"] = "Loopback" + input("Numero de interfaz: ")
    nueva_interface["desc"] = input("Descripcion: ")
    nueva_interface["status"] = "true"
    nueva_interface["ip_address"] = input("Dirección: ")
    nueva_interface["mask"] = input("Mascara de subred: ")
    
    # Rellenamos la plantilla con los nuevos datos
    netconf_data = plantilla_interface.format(
            name = nueva_interface["name"],
            desc = nueva_interface["desc"],
            #type = nueva_interface["type"],
            status = nueva_interface["status"],
            ip_address = nueva_interface["ip_address"],
            mask = nueva_interface["mask"]
        )
    
    # Lanzamos peticion
    print("Creamos interface ", nueva_interface["name"])
    try:
        netconf_reply = con.edit_config(netconf_data, target = 'running') 
    except:
        print("Ha habido algún error creando la interface ", nueva_interface["name"])

def borraInterface():
    # Reusamos la funcion del ej1 para consultar y listar las interfaces de tipo Loopback
    interfaces = obtenInterfaces()

    listaInterfacesLoopbackCreadas = []

    for i in interfaces:
        if i[0].startswith("Loopback"):
            listaInterfacesLoopbackCreadas.append(i[0])

    # Definimos conexión
    con = manager.connect(host=deviceIP,port=830,username=username,password=password,hostkey_verify=False)
    
    plantilla_interface = """
     <config>
         <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
             <interface operation="delete">
                 <name>{name}</name>
             </interface>
         </interfaces>
     </config>"""
    
    # Mostramos el listado de posibles interfaces a borrar
    print("Interfaces Loopback:")
    pprint.pprint(listaInterfacesLoopbackCreadas)

    interfaceAborrar = {}
    interfaceAborrar["name"] = "Loopback" + input("¿Que número de loopback eliminamos? ")

    # Actualizamos los datos en la interfaz
    netconf_data = plantilla_interface.format(
            name = interfaceAborrar["name"])
    
    # Ejecutamos
    try:
        print("Eliminamos la interface ", interfaceAborrar["name"])
        netconf_reply = con.edit_config(netconf_data, target = 'running')
    except:
        print("Hubo algun error eliminando la interface ", interfaceAborrar["name"])


def obtenRutas():
    filtroNetconf ="""
    <filter>
    <routing xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"/>
    </filter>
    """

    detalleRuta = []
    listaRutas = []

    with manager.connect_ssh(host=deviceIP, port=830, username=username, hostkey_verify=False, password=password) as m:
        try:
            resp = m.get(filtroNetconf).data_xml
            resp_parseado = xmltodict.parse(resp)

            tipo = resp_parseado["data"]["routing"]["routing-instance"]["routing-protocols"]["routing-protocol"]["type"]
            destino = resp_parseado["data"]["routing"]["routing-instance"]["routing-protocols"]["routing-protocol"]["static-routes"]["ipv4"]["route"]["destination-prefix"]
            interfaceSalida = resp_parseado["data"]["routing"]["routing-instance"]["routing-protocols"]["routing-protocol"]["static-routes"]["ipv4"]["route"]["next-hop"]["outgoing-interface"]
            
            detalleRuta = (tipo, destino, interfaceSalida)
            listaRutas.append(detalleRuta)


            print(tabulate(listaRutas))

        except Exception as e:
            print('Hubo problemas obteniendo rutas: {}'.format(e))

            

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

    # Obtener un listado de las interfaces
    if opcion_elegida == '1':
        listado = obtenInterfaces()
        print(tabulate(listado))

    # Crear Interfaces       
    if opcion_elegida == '2':
        creaInterface()

    # Borrar Interfaces       
    if opcion_elegida == '3':
        borraInterface()        

    # Obtener rutas      
    if opcion_elegida == '4':
        obtenRutas() 


    # Opcion salir
    elif opcion_elegida == '5':
        print("Hasta la proxima!")
        sys.exit(0)












# Ejecutamos el programa
if __name__== "__main__":
    while True:
        main()


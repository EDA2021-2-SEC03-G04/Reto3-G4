"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf

default_limit=1000
sys.setrecursionlimit(default_limit*10)


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2-(REQ1) Contar los avistamientos en una ciudad ")
    print("3-(REQ2)  Contar los avistamientos por duración ")
    print("4-(REQ3)  Contar avistamientos por Hora/Minutos del día")
    print('5-(REQ4)  Contar los avistamientos en un rango de fechas')
    print('6-(REQ5)  Contar los avistamientos de una Zona Geográfica')
    print('7-(BONO)  Visualizar los avistamientos de una zona geográfica.')


def printEspacio():
    """
    añade espacios entre funciones 
    """

    print("")
    print("=" * 100)
    print("")
    

catalog = None

def printAvistamientosHHMM(size,Pequenos,Grandes,liminf,limsup):
    print()
    print(f'Hay {size} Avistamientos en el rango [{liminf}-{limsup}] ')
    print()
    print('Top 3 avistamientos más recientes:  ')
    print()
    i=1
    for Elto in lt.iterator(Pequenos):
        print('Avistamiento ' + str(i) + ')--- con fecha: ' + str(Elto['datetime']) + ' , país: ' + str(Elto['country']) + ' y ciudad: ' + str(Elto['city']) + ', duración (segs): ' + str(Elto['durationS']) + 'con forma : ' + str(Elto['shape']))
        i=i+1
    print()
    print('Top 3 avistamientos más antiguos:  ')
    print()
    i=1
    for Elto in lt.iterator(Grandes):
        print('Avistamiento ' + str(i) + ')--- con fecha: ' + str(Elto['datetime']) + ' , país: ' + str(Elto['country']) + ' y ciudad: ' + str(Elto['city']) + ', duración (segs): ' + str(Elto['durationS']) + 'con forma : ' + str(Elto['shape']))
        i=i+1



def printAvistamientosDMA(oldestSize,oldestKey,size,Pequenos,Grandes,liminf,limsup):
    print()
    print(f'Hay {size} Avistamientos en el rango [{liminf} , {limsup}] ')
    print()
    print('Top 3 avistamientos más recientes:  ')
    print()
    i=1
    for Elto in lt.iterator(Pequenos):
        print('Avistamiento ' + str(i) + ')--- con fecha: ' + str(Elto['datetime']) + ' , país: ' + str(Elto['country']) + ' y ciudad: ' + str(Elto['city']) + ', duración (segs): ' + str(Elto['durationS']) + 'con forma : ' + str(Elto['shape']))
        i=i+1
    print()
    print('Top 3 avistamientos más antiguos:  ')
    print()
    i=1
    for Elto in lt.iterator(Grandes):
        print('Avistamiento ' + str(i) + ')--- con fecha: ' + str(Elto['datetime']) + ' , país: ' + str(Elto['country']) + ' y ciudad: ' + str(Elto['city']) + ', duración (segs): ' + str(Elto['durationS']) + 'con forma : ' + str(Elto['shape']))
        i=i+1
    print()
    print()
    print('La fecha más vieja registrada es ' + str(oldestKey) + ' con ' + str(oldestSize) + ' avistamiento(s) ')
    print()
    print()




def printAvistamienCiudad(datos, lugar):
    print("para la ciudad " + lugar + " hay " + str(lt.size(datos)) + " avistamientos")
    print()
    print("Top 3 Primeros: ")
    for x in range(3):
        mom = x+1
        ob = lt.getElement(datos, mom)
        print("El dia " + ob["datetime"] + " en la ciudad de " + ob["city"] + " EN el estado de " + ob["state"] + " EN la ciudad " + ob["country"] + " suirgio un avistamiento de " + ob["shape"] + " forma y " + ob["durationHM"] + " duracion")

    print()
    print("Top 3 ultimos: ")

    for x in range(3):
        mom = x+1
        ob = lt.getElement(datos, lt.size(datos)-x)
        print("El dia " + ob["datetime"] + " en la ciudad de " + ob["city"] + " EN el estado de " + ob["state"] + " EN la ciudad " + ob["country"] + " suirgio un avistamiento de " + ob["shape"] + " forma y " + ob["durationHM"] + " duracion")

def printAvistamienDireccion(retorno, limInf, limSup):
    
    print("en el rango " + str(limInf) + " a " + str(limSup) + " hay " + str(lt.size(retorno[0])) + " avistamientos")
    print()
    print("La mayor duracion es " + str(retorno[1][0]) + " con " + str(retorno[1][1]) + " avistamientos")
    print()
    print("Top 3 Primeros: ")

    for x in range(3):
        mom = x+1
        ob = lt.getElement(retorno[0], mom)
        print("El dia " + ob["datetime"] + " en la ciudad de " + ob["city"] + " EN el estado de " + ob["state"] + " EN la ciudad " + ob["country"] + " suirgio un avistamiento de " + ob["shape"] + " forma y " + ob["durationS"] + " duracion")
    
    print()
    print("Top 3 Ultimos: ")
    for x in range(3):
        mom = x+1
        ob = lt.getElement(retorno[0], lt.size(retorno[0])-x)
        print("El dia " + ob["datetime"] + " en la ciudad de " + ob["city"] + " EN el estado de " + ob["state"] + " EN la ciudad " + ob["country"] + " suirgio un avistamiento de " + ob["shape"] + " forma y " + ob["durationS"] + " duracion")
    
def printAvistamienCordenadas(retorno):

    print("En el rango dado se encontraron " + str(lt.size(retorno)) + " avistamientos")
    print()
    print("Top 5 Primeros: ")

    for x in range(3):
        mom = x+1
        ob = lt.getElement(retorno, mom)
        print("El dia " + ob["datetime"] + " en la ciudad de " + ob["city"] + " EN el estado de " + ob["state"] + " EN la ciudad " + ob["country"] + " suirgio un avistamiento de " + ob["shape"] + " forma y " + ob["durationS"] + " duracion, con la latitud " + ob["latitude"] + " y longitud " + ob["longituide"])                                                                                             

    print()
    print("Top 5 Ultimos: ")

    for x in range(3):
        mom = x+1
        ob = lt.getElement(retorno, lt.size(retorno)-x)
        print("El dia " + ob["datetime"] + " en la ciudad de " + ob["city"] + " EN el estado de " + ob["state"] + " EN la ciudad " + ob["country"] + " suirgio un avistamiento de " + ob["shape"] + " forma y " + ob["durationS"] + " duracion, con la latitud " + ob["latitude"] + " y longitud " + ob["longituide"])


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.init()
        print("\nCargando información de UFOS ....")
        controller.loadData(catalog)
        print('Ciudades cargados: ' + str(controller.citiesSize(catalog)))
        print('Altura del arbol: ' + str(controller.indexHeight(catalog)))
        print('Elementos en el arbol: ' + str(controller.indexSize(catalog)))
        print('Menor Llave: ' + str(controller.minKey(catalog)))
        print('Mayor Llave: ' + str(controller.maxKey(catalog)))


    elif int(inputs[0]) == 2:
        
        printEspacio()

        ciudad = input("De que ciudad deseas buscar: ")
        retorno = controller.AvistamienCiudad(catalog,ciudad)
        print()
        print()
        print('='*42 + ' RESPUESTA REQ 1 ' + '='*42)
        print()

        printAvistamienCiudad(retorno, ciudad)

        printEspacio()


    elif int(inputs[0]) == 3:
        
        printEspacio()

        limInf = float(input("Cual es el limite inferior en segundos?: "))
        limSup = float(input("Cual es el limite superior en segundos?: "))
        retorno = controller.AvistamienDireccion(catalog, limInf, limSup)
        print()
        print()
        print('='*42 + ' RESPUESTA REQ 2 ' + '='*42)
        print()

        printAvistamienDireccion(retorno, limInf, limSup)

        printEspacio()

    
    elif int(inputs[0])==4:
        printEspacio()

        liminf=input('Ingrese el limite inferior en formato HH:MM: ')
        limsup=input('Ingrese el límite superior en formateo HH:MM: ')
        size,Pequenos,Grandes=controller.AvistamientoHHMM(catalog,liminf,limsup)
        print()
        print()
        print('='*42 + ' RESPUESTA REQ 3 ' + '='*42)
        printAvistamientosHHMM(size,Pequenos,Grandes,liminf,limsup)

        printEspacio()

    elif int(inputs[0])==5:

        printEspacio()
        liminf=input('Ingrese el limite inferior en formato AAAA-MM-DD: ')
        limsup=input('Ingrese el límite superior en formateo AAAA-MM-DD: ')
        oldestSize,oldestkey,size,Pequenos,Grandes=controller.AvistamientoDMA(catalog,liminf,limsup)
        print()
        print()
        print('='*42 + ' RESPUESTA REQ 4 ' + '='*42)
        printAvistamientosDMA(oldestSize,oldestkey,size,Pequenos,Grandes,liminf,limsup)


    elif int(inputs[0]) == 6:
        
        printEspacio()

        LonglimInf = float(input("Cual es el limite inferior de la longitud?: "))
        LonglimSup = float(input("Cual es el limite superior de la longitud?: "))
        print()
        LatlimInf = float(input("Cual es el limite inferior de la latitud?: "))
        LatlimSup = float(input("Cual es el limite superior de la latitud?: "))
        retorno = controller.AvistamienCordenadas(catalog, LonglimInf, LonglimSup, LatlimInf, LatlimSup)
        print()
        print()
        print('='*42 + ' RESPUESTA REQ 5 ' + '='*42)
        print()

        printAvistamienCordenadas(retorno)

        printEspacio() 
        



    else:
        sys.exit(0)
sys.exit(0)

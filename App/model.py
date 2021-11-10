﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mrgsort
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as m
import datetime
assert cf
import itertools

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    catalog = {'UFOSByCity': None
        
                }

    #MAP para el REQ1, llaves ciudad, values: lista con avistamientos de esa ciudad
    catalog['UFOSByCity'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareCities)

    #MAP para el REQ2. llaves: duracion por segundos. values: lista de avistamientos con esa duración
    catalog['UFOSBySeconds'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDurationSegs)
    
    #MAP para el REQ3. llaves: avistamiento por HH:MM. values: lista de avistamientos con esta fecha
    catalog['UFOSByHHMM'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareHHMM)
    catalog['UFOSByDMA']=om.newMap(omaptype='RBT',comparefunction=compareDates)

    catalog['UFOSByLONG']=om.newMap(omaptype='RBT',comparefunction=compareLong)
    


    return catalog

# Funciones para agregar informacion al catalogo

def addUFO(catalog,UFO):
    new=newUFO(UFO['datetime'],UFO['city'],UFO['state'],UFO['country'],UFO['shape'],UFO['duration (seconds)'],UFO['duration (hours/min)'],UFO['comments'],UFO['date posted'],UFO['latitude'],UFO['longitude'])

    #Crea el tree de UFOS por ciudades
    City=UFO['city']
    entry1=om.contains(catalog['UFOSByCity'],City)
    #Date=UFO['datetime']
    #Datetime=datetime.datetime.strptime(Date, '%Y-%m-%d %H:%M:%S')
    createMAP(City,new,'UFOSByCity',entry1,catalog)


    #Crea el tree de UFOS por duración en segs
    Duration=UFO['duration (seconds)']
    Duration=int(float(Duration))
    entry2=om.contains(catalog['UFOSBySeconds'],Duration)
    createMAP(Duration,new,'UFOSBySeconds',entry2,catalog)


    #Crea el tree de UFOS por HHMM
    Date1=UFO['datetime']
    Date11=transformHHMM(Date1)
    entry3=om.contains(catalog['UFOSByHHMM'],Date11)
    createMAP(Date11,new,'UFOSByHHMM',entry3,catalog)


    #Crea el tree de UFOS por DMA
    Date2=UFO['datetime']
    Date22=transformDMA(Date2)
    entry4=om.contains(catalog['UFOSByDMA'],Date22)
    createMAP(Date22,new,'UFOSByDMA',entry4,catalog)

    #crea el tree de UFOS por longitud
    long1=round(float(UFO["longitude"]),2)
    entry5=om.contains(catalog['UFOSByLONG'],long1)
    createMAP(long1,new,'UFOSByLONG',entry5,catalog)







def createMAP(key,value,mapname,entry,catalog): 
    '''
    Crea un mapa con llaves keys y values listas 
    '''

    if entry: 
        listavieja=om.get(catalog[mapname],key)['value']
        
        #mapaviejo=om.get(catalog['UFOSByCity'],City)
        #om.put(mapaviejo,City,new)
        lt.addLast(listavieja,value)
        om.put(catalog[mapname],key,listavieja)
        #om.put(catalog['UFOSByCity'],City,mapaviejo)
    else: 
        lista=lt.newList()
        #mapa=om.newMap(omaptype='RBT',comparefunction=compareDates)
        lt.addLast(lista,value)
        #om.put(mapa,Datetime,new)
        #om.put(catalog['UFOSByCity'],City,mapa)
        om.put(catalog[mapname],key,lista)

    



# Funciones para creacion de datos

def newUFO(datetime,city,state,country,shape,durationS,durationHM,comments,dateposted,latitude,longitude):

    UFO={'datetime':'','city':'','state':'','country':'','shape':'','durationS':'','durationHM':''
    ,'comments':'','dateposted':'','latitude':'','longitude':''}

    UFO['datetime']=datetime
    UFO['city']=city
    UFO['state']=state
    UFO['country']=country
    UFO['shape']=shape
    UFO['durationS']=durationS
    UFO['durationHM']=durationHM
    UFO['comments']=comments
    UFO['dateposted']=dateposted
    UFO['latitude']=latitude
    UFO['longituide']=longitude

    return UFO



# Funciones de consulta

def citiesSize(catalog):
    """
    Número de crimenes
    """
    return om.size(catalog['UFOSByCity'])


def indexHeight(catalog):
    """
    Altura del arbol
    """
    return om.height(catalog['UFOSByCity'])


def indexSize(catalog):
    """
    Numero de elementos en el indice
    """
    return om.size(catalog['UFOSByCity'])


def minKey(catalog):
    """
    Llave mas pequena
    """
    return om.minKey(catalog['UFOSByCity'])


def maxKey(catalog):
    """
    Llave mas grande
    """
    return om.maxKey(catalog['UFOSByCity'])


def AvistamientoHHMM(catalog,liminf,limsup):

    '''
    Retorna la cantidad de avitamientos en el rango [liminf,limsup] y el top 3 
    y más recientes y antiguos avistamientos en ese rango
    '''
    
    map=catalog['UFOSByHHMM']
    #print(map)
    KeysInRange=om.values(map,liminf,limsup)
    KeysInRangeFlat=lt.newList(cmpfunction=compByDateFormat)
    

    for Element in lt.iterator(KeysInRange):
        for Element2 in lt.iterator(Element):
            lt.addLast(KeysInRangeFlat,Element2)

    mrgsort.sort(KeysInRangeFlat,compByDateFormat)

    size=lt.size(KeysInRangeFlat)

    Pequenos=lt.newList()
    Grandes=lt.newList()

    for x in range(3):
        if size > x:
            lt.addLast(Pequenos,lt.getElement(KeysInRangeFlat,x))
        else:
            True
    
    for x in range(3):
        if size-x > 0:
            lt.addLast(Grandes,lt.getElement(KeysInRangeFlat,size-x))
        else:
            True

    
    return size,Pequenos,Grandes

def AvistamientoAMD(catalog,liminf,limsup):


    '''
    Retorna la cantidad de avitamientos en el rango [liminf,limsup] y el top 3 
    y más recientes y antiguos avistamientos en ese rango
    '''
    
    map=catalog['UFOSByDMA']
    KeysInRange=om.values(map,liminf,limsup)
    KeysInRangeFlat=lt.newList(cmpfunction=compByDateFormat)

    oldestKey=om.minKey(map)
    oldestElement=om.get(map,oldestKey)['value']
    oldestSize=lt.size(oldestElement)
    

    for Element in lt.iterator(KeysInRange):
        for Element2 in lt.iterator(Element):
            lt.addLast(KeysInRangeFlat,Element2)

    mrgsort.sort(KeysInRangeFlat,compByDateFormat)

    size=lt.size(KeysInRangeFlat)

    Pequenos=lt.newList()
    Grandes=lt.newList()

    for x in range(3):
        if size > x:
            lt.addLast(Pequenos,lt.getElement(KeysInRangeFlat,x))
        else:
            True
    
    for x in range(3):
        if size-x > 0:
            lt.addLast(Grandes,lt.getElement(KeysInRangeFlat,size-x))
        else:
            True

    
    return oldestSize,oldestKey,size,Pequenos,Grandes



def AvistamienCiudad(catalog,ciudad):
    principal = catalog['UFOSByCity']
    espesifico = om.get(principal, ciudad)["value"]

    mrgsort.sort(espesifico,compByDateFormat)

    return espesifico

    
def AvistamienDireccion(catalog, limInf, limSup):
    principal = catalog['UFOSBySeconds']
    retorno = lt.newList()

    listaVal = [limInf]
    val1 = limInf
    val2 = limSup

    maximoLL = om.maxKey(principal)
    maximoComp = om.get(principal, maximoLL)["value"]
    maximoCant = lt.size(maximoComp)

    while val1 < val2:
        val1 += 1
        listaVal.append(val1)
    
    for x in listaVal:

        if om.contains(principal, float(x)):   

            espesifico = om.get(principal, x)["value"]

            for x in range(lt.size(espesifico)):

                elemento = lt.getElement(espesifico, x+1)
                lt.addLast(retorno, elemento)
    
    

    return [retorno, [maximoLL, maximoCant]]
    
    
def AvistamienCordenadas(catalog, LonglimInf, LonglimSup, LatlimInf, LatlimSup):
    principal = catalog["UFOSByLONG"]
    retorno = lt.newList()

    KeysRangoLong = om.keys(principal, LonglimSup, LonglimInf)

    for x in range(lt.size(KeysRangoLong)):

        espesifico = om.get(principal,lt.getElement(KeysRangoLong, x+1))["value"]

        for y in range(lt.size(espesifico)):

            avis = lt.getElement(espesifico, y+1)

            if round(float(avis["latitude"]), 2) > LatlimInf and round(float(avis["latitude"]), 2) < LatlimSup: 

                lt.addLast(retorno, avis)

    return retorno 




   

# Funciones utilizadas para comparar elementos dentro de una lista

def transformHHMM(HMS):
    '''
    Transorma 6/01/2001 18:30 de string a 18:30 en datetime
    Si es vacio le asigna la HHMM=00:00

    '''
    try:
        date2=HMS.split(' ')
        date3=date2[1]
        HMDateTime = datetime.datetime.strptime(date3, '%H:%M')
        return HMDateTime
        
    except:
        HMDateTime=datetime.datetime.strptime('00:00', '%H:%M')
        return HMDateTime

def transformDMA(Date):
    '''
    Transorma 6/01/2001 18:30 de string a 06/01/2001 en datetime
    Si es vacio le asigna la DMA=2022/11/21

    '''

    

    try:
        date2=Date.split()
        date3=date2[0]
        
        DMADateTime = datetime.datetime.strptime(date3, "%Y-%m-%d")
        
        return DMADateTime
        
    except:
        
        DMADateTime=datetime.datetime.strptime('2022/11/21',"%Y-%m-%d")
        
        return DMADateTime

        
    

def compareCities(city1,city2):
    '''
    Compara ciudades
    '''
    
    if (city1.lower()==city2.lower()):
        return 0
    elif (city1.lower() > city2.lower()):
        return 1
    else:
        return -1

def compareDates(date1,date2): 
    '''
    Compara Fechas en formato AAAA-MM-DD HH:MM

    '''
    if (date1==date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareLong(long1,long2): 
    '''
    Compara longitudes 

    '''
    if (long1==long2):
        return 0
    elif (long1 > long2):
        return 1
    else:
        return -1

def compareDurationSegs(time1,time2): 
    '''
    Compara duraciones en tamaño int

    '''
    if (time1==time2):
        return 0
    elif (time1 > time2):
        return 1
    else:
        return -1

def compareHHMM(HM1,HM2):
    '''
    Compara duraciones en tamaño int

    '''
    #if (HM1==HM2):
        #return 0
    #elif (HM1 > HM2):
        #return 1
    #else:
        #return -1
    return HM1<HM2

def compByDateFormat(d1,d2):

    d1 = d1['datetime'].split()
    d1F = datetime.datetime.strptime(d1[0], "%Y-%m-%d")
    d2 = d2['datetime'].split()
    d2F = datetime.datetime.strptime(d2[0], "%Y-%m-%d")

    return d1F < d2F

    



# Funciones de ordenamiento


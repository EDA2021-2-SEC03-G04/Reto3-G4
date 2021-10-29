"""
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
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as m
import datetime
assert cf

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


    return catalog

# Funciones para agregar informacion al catalogo

def addUFO(catalog,UFO):
    new=newUFO(UFO['datetime'],UFO['city'],UFO['state'],UFO['country'],UFO['shape'],UFO['duration (seconds)'],UFO['duration (hours/min)'],UFO['comments'],UFO['date posted'],UFO['latitude'],UFO['longitude'])

    #Crea el tree de UFOS por ciudades
    City=UFO['city']
    entry1=om.get(catalog['UFOSByCity'],City)
    #Date=UFO['datetime']
    #Datetime=datetime.datetime.strptime(Date, '%Y-%m-%d %H:%M:%S')
    createMAP(City,new,'UFOSByCity',entry1,catalog)


    #Crea el tree de UFOS por duración en segs
    Duration=UFO['duration (seconds)']
    Duration=int(float(Duration))
    entry2=om.get(catalog['UFOSBySeconds'],Duration)
    createMAP(Duration,new,'UFOSBySeconds',entry2,catalog)









def createMAP(key,value,mapname,entry,catalog): 
    '''
    Crea un mapa con llaves keys y values listas 
    '''

    if not(entry is None): 
        listavieja=om.get(catalog[mapname],key)
        #mapaviejo=om.get(catalog['UFOSByCity'],City)
        #om.put(mapaviejo,City,new)
        lt.addLast(listavieja['value'],value)
        om.put(catalog[mapname],key,listavieja['value'])
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

# Funciones utilizadas para comparar elementos dentro de una lista
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



    



# Funciones de ordenamiento

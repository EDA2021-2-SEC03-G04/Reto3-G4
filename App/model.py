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
    #Toma el map ordenado por HHMM
    map=catalog['UFOSByHHMM']
    #Extrae las llaves en el rango lim inf, lim sup
    KeysInRange=om.values(map,liminf,limsup)


    #Iniciliza las fechas máximss y sus correspondientes ufos y las fechas mínimas con sus correspondientes ufos

    maxC1=datetime.datetime.strptime('1700-03-21', "%Y-%m-%d")
    maxC2=datetime.datetime.strptime('1700-03-21', "%Y-%m-%d")
    maxC3=datetime.datetime.strptime('1700-03-21', "%Y-%m-%d")
    maxC4=datetime.datetime.strptime('1700-03-21', "%Y-%m-%d")
    maxC5=datetime.datetime.strptime('1700-03-21', "%Y-%m-%d")

    eltoC1={'datetime':'','city':'','state':'','country':'','shape':'','durationS':'','durationHM':''
    ,'comments':'','dateposted':'','latitude':'','longitude':''}


    eltoC2=eltoC3=eltoC4=eltoC5=eltoP1=eltoP2=eltoP3=eltoP4=eltoP5=eltoC1

    maxP1=datetime.datetime.strptime('2021-03-21', "%Y-%m-%d")
    maxP2=datetime.datetime.strptime('2021-03-21', "%Y-%m-%d")
    maxP3=datetime.datetime.strptime('2021-03-21', "%Y-%m-%d")
    maxP4=datetime.datetime.strptime('2021-03-21', "%Y-%m-%d")
    maxP5=datetime.datetime.strptime('2021-03-21', "%Y-%m-%d")
    

    i=0
    for Element in lt.iterator(KeysInRange):
        
        for Element2 in lt.iterator(Element):
            i=i+1
            Date=transformDMA(Element2['datetime'])
            

            if Date>maxC1:
                eltoC5=eltoC4
                maxC5=maxC4

                eltoC4=eltoC3
                maxC4=maxC3

                eltoC3=eltoC2
                maxC3=maxC2

                eltoC2=eltoC1
                maxC2=maxC1
                

                eltoC1=Element2
                maxC1=Date
       
            elif Date>maxC2:

                eltoC5=eltoC4
                maxC5=maxC4

                eltoC4=eltoC3
                maxC4=maxC3

                eltoC3=eltoC2
                maxC3=maxC2



                eltoC2=Element2
                maxC2=Date
            elif Date>maxC3:

                eltoC5=eltoC4
                maxC5=maxC4

                eltoC4=eltoC3
                maxC4=maxC3


                eltoC3=Element2
                maxC3=Date
            elif Date>maxC4:
                eltoC4=Element2
                maxC4=Date
            elif Date>maxC5:
                eltoC5=Element2
                maxC5=Date




            if Date < maxP1:

                eltoP5=eltoP4
                maxP5=maxP4

                eltoP4=eltoP3
                maxP4=maxP3

                eltoP3=eltoP2
                maxP3=maxP2

                eltoP2=eltoP1
                maxP2=maxP1


                eltoP1=Element2
                maxP1=Date

            elif Date<maxP2:
                eltoP5=eltoP4
                maxP5=maxP4

                eltoP4=eltoP3
                maxP4=maxP3

                eltoP3=eltoP2
                maxP3=maxP2



                eltoP2=Element2
                maxP2=Date
            elif Date<maxP3:

                eltoP5=eltoP4
                maxP5=maxP4

                eltoP4=eltoP3
                maxP4=maxP3



                eltoP3=Element2
                maxP3=Date
            elif Date<maxP4:

                eltoP5=eltoP4
                maxP5=maxP4



                eltoP4=Element2
                maxP4=Date
            elif Date<maxP5:

                eltoP5=Element2
                maxP5=Date

    #Se guardan en listas los UFOS con fecha máxima y lOS ufos  con fecha mínima
    Pequenos=lt.newList()
    Grandes=lt.newList()
    lt.addLast(Pequenos,eltoC1)
    lt.addLast(Pequenos,eltoC2)
    lt.addLast(Pequenos,eltoC3)
    lt.addLast(Pequenos,eltoC4)
    lt.addLast(Pequenos,eltoC5)

    lt.addLast(Grandes,eltoP1)
    lt.addLast(Grandes,eltoP2)
    lt.addLast(Grandes,eltoP3)
    lt.addLast(Grandes,eltoP4)
    lt.addLast(Grandes,eltoP5)   

    size=i
    
    return size,Pequenos,Grandes

def AvistamientoAMD(catalog,liminf,limsup):


    '''
    Retorna la cantidad de avitamientos en el rango [liminf,limsup] y el top 3 
    y más recientes y antiguos avistamientos en ese rango
    '''
    
    map=catalog['UFOSByDMA']
    KeysInRange=om.values(map,liminf,limsup)
    #KeysInRangeFlat=lt.newList(cmpfunction=compByDateFormat)

    oldestKey=om.minKey(map)
    oldestElement=om.get(map,oldestKey)['value']
    oldestSize=lt.size(oldestElement)

    #Iniciliza las fechas máximss y sus correspondientes ufos y las fechas mínimas con sus correspondientes ufos

    maxC1=datetime.datetime.strptime('1700-03-21', "%Y-%m-%d")
    maxC2=datetime.datetime.strptime('1700-03-21', "%Y-%m-%d")
    maxC3=datetime.datetime.strptime('1700-03-21', "%Y-%m-%d")
    maxC4=datetime.datetime.strptime('1700-03-21', "%Y-%m-%d")
    maxC5=datetime.datetime.strptime('1700-03-21', "%Y-%m-%d")

    eltoC1={'datetime':'','city':'','state':'','country':'','shape':'','durationS':'','durationHM':''
    ,'comments':'','dateposted':'','latitude':'','longitude':''}


    eltoC2=eltoC3=eltoC4=eltoC5=eltoP1=eltoP2=eltoP3=eltoP4=eltoP5=eltoC1

    maxP1=datetime.datetime.strptime('2021-03-21', "%Y-%m-%d")
    maxP2=datetime.datetime.strptime('2021-03-21', "%Y-%m-%d")
    maxP3=datetime.datetime.strptime('2021-03-21', "%Y-%m-%d")
    maxP4=datetime.datetime.strptime('2021-03-21', "%Y-%m-%d")
    maxP5=datetime.datetime.strptime('2021-03-21', "%Y-%m-%d")
    

    i=0
    for Element in lt.iterator(KeysInRange):
        
        for Element2 in lt.iterator(Element):
            i=i+1
            Date=transformDMA(Element2['datetime'])
            

            if Date>maxC1:
                eltoC5=eltoC4
                maxC5=maxC4

                eltoC4=eltoC3
                maxC4=maxC3

                eltoC3=eltoC2
                maxC3=maxC2

                eltoC2=eltoC1
                maxC2=maxC1
                

                eltoC1=Element2
                maxC1=Date
       
            elif Date>maxC2:

                eltoC5=eltoC4
                maxC5=maxC4

                eltoC4=eltoC3
                maxC4=maxC3

                eltoC3=eltoC2
                maxC3=maxC2



                eltoC2=Element2
                maxC2=Date
            elif Date>maxC3:

                eltoC5=eltoC4
                maxC5=maxC4

                eltoC4=eltoC3
                maxC4=maxC3


                eltoC3=Element2
                maxC3=Date
            elif Date>maxC4:
                eltoC4=Element2
                maxC4=Date
            elif Date>maxC5:
                eltoC5=Element2
                maxC5=Date




            if Date < maxP1:

                eltoP5=eltoP4
                maxP5=maxP4

                eltoP4=eltoP3
                maxP4=maxP3

                eltoP3=eltoP2
                maxP3=maxP2

                eltoP2=eltoP1
                maxP2=maxP1


                eltoP1=Element2
                maxP1=Date

            elif Date<maxP2:
                eltoP5=eltoP4
                maxP5=maxP4

                eltoP4=eltoP3
                maxP4=maxP3

                eltoP3=eltoP2
                maxP3=maxP2



                eltoP2=Element2
                maxP2=Date
            elif Date<maxP3:

                eltoP5=eltoP4
                maxP5=maxP4

                eltoP4=eltoP3
                maxP4=maxP3



                eltoP3=Element2
                maxP3=Date
            elif Date<maxP4:

                eltoP5=eltoP4
                maxP5=maxP4



                eltoP4=Element2
                maxP4=Date
            elif Date<maxP5:

                eltoP5=Element2
                maxP5=Date

    #Se guardan en listas las obras con precio máximo y las obras con fecha mínima
    Pequenos=lt.newList()
    Grandes=lt.newList()
    lt.addLast(Pequenos,eltoC1)
    lt.addLast(Pequenos,eltoC2)
    lt.addLast(Pequenos,eltoC3)
    lt.addLast(Pequenos,eltoC4)
    lt.addLast(Pequenos,eltoC5)

    lt.addLast(Grandes,eltoP1)
    lt.addLast(Grandes,eltoP2)
    lt.addLast(Grandes,eltoP3)
    lt.addLast(Grandes,eltoP4)
    lt.addLast(Grandes,eltoP5)   

           
    
    
    size=i


    

    
    
    return oldestSize,oldestKey,size,Pequenos,Grandes



def AvistamienCiudad(catalog,ciudad):
    '''
    Devuelve todos los avistamientos de una ciudad y los organiza por fecha
    '''
    #Map ordenado por ciudades
    principal = catalog['UFOSByCity']
    #Extrae la llave de la ciudad que se está buscando
    especifico = om.get(principal, ciudad)["value"]
    #Ordena los avistamientos por fecha 
    mrgsort.sort(especifico,compByDateFormat)

    return especifico

    
def AvistamienDireccion(catalog, limInf, limSup):
    '''
    Retorna los avistamientos por duración [liminf,limsup] y los ordena por esa duración. 
    '''
    #Toma el map ordenado por duración
    principal = catalog['UFOSBySeconds']
    retorno = lt.newList()

    listaVal = [limInf]
    val1 = limInf
    val2 = limSup
    #Toma la llave máxima del map y su value y cuantos avistamientos tiene
    maximoLL = om.maxKey(principal)
    maximoComp = om.get(principal, maximoLL)["value"]
    maximoCant = lt.size(maximoComp)

    while val1 < val2:
        val1 += 1
        listaVal.append(val1)
    #Recorre las duraciones entre limInf y limSup  y toma sus }
    # avistamientos para añadirlos a retorno (Ya quedan ordenados)
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
        HMDateTime = datetime.datetime.strptime(date3, '%H:%M:%S')
        return HMDateTime
        
    except:
        HMDateTime=datetime.datetime.strptime('00:00:00', '%H:%M:%S')
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
    if (HM1==HM2):
        return 0
    elif (HM1 > HM2):
        return 1
    else:
        return -1
    #return HM1<HM2

def compByDateFormat(d1,d2):

    d1 = d1['datetime'].split()
    d1F = datetime.datetime.strptime(d1[0], "%Y-%m-%d")
    d2 = d2['datetime'].split()
    d2F = datetime.datetime.strptime(d2[0], "%Y-%m-%d")

    return d1F < d2F

    



# Funciones de ordenamiento


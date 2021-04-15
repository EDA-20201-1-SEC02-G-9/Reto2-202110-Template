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
import csv
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import linkedlistiterator as lliterator
from DISClib.DataStructures import arraylistiterator as aliterator
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def has_tag(video, tag):
        return lt.isPresent(video[1], tag)

def add_to_top(video, top, k: int):
    iter_video = top['first']
    while iter_video['next'] and lt.getElement(video[0], k) > lt.getElement(iter_video['next']['info'][0], k):
        iter_video = iter_video['next']
    next = iter_video['next']
    iter_video['next'] = {'info': video, 'next': next}
    if not next:
        top['last'] = iter_video['next']
    top['size'] += 1

def if_add_video_req(video, top, k:int, n: int):
    min_top = None
    if not lt.isEmpty(top):
        min_top = lt.firstElement(top)
    if not min_top:
        lt.addFirst(top, video)
    # ... or likesVideo > likesMinTop:
    elif lt.size(top) < n or lt.getElement(video[0], k) > lt.getElement(min_top[0], k):
        add_to_top(video, top, k)
    if lt.size(top) > n:
        lt.removeFirst(top)

class catalog_iterator:
    def __init__(self, catalog):
        super_list = mp.valueSet(catalog.videos)
        self.super_iter = lliterator.newIterator(super_list)
        country_map = lliterator.next(self.super_iter)
        country_list = mp.valueSet(country_map)
        self.country_iter = lliterator.newIterator(country_list)
        self.category_iter = aliterator.newIterator(lliterator.next(self.country_iter))

    
    def __next__(self):
        while not aliterator.hasNext(self.category_iter):
            while not lliterator.hasNext(self.country_iter):
                if not lliterator.hasNext(self.super_iter):
                    raise StopIteration
                else:
                    country_list = mp.valueSet(lliterator.next(self.super_iter))
                    self.country_iter = lliterator.newIterator(country_list)
            self.category_iter = aliterator.newIterator(lliterator.next(self.country_iter))
        current = aliterator.next(self.category_iter)
        return current

class country_iterator:
    def __init__(self, catalog, country):
        country_map = mp.get(catalog.videos, country)['value']
        country_list = mp.valueSet(country_map)
        self.country_iter = lliterator.newIterator(country_list)
        self.category_iter = aliterator.newIterator(lliterator.next(self.country_iter))
    
    def __next__(self):
        while not aliterator.hasNext(self.category_iter):
            if not lliterator.hasNext(self.country_iter):
                raise StopIteration
            else:
                self.category_iter = aliterator.newIterator(lliterator.next(self.country_iter))
        current = aliterator.next(self.category_iter)
        return current
    
    def __iter__(self):
        return self

class country_category_iterator:
    def __init__(self, catalog, country, category):
        country_map = mp.get(catalog.videos, country)['value']
        category_list = mp.get(country_map, category)['value']
        self.category_iter = aliterator.newIterator(category_list)
    
    def __next__(self):
        if not aliterator.hasNext(self.category_iter):
            raise StopIteration
        current = aliterator.next(self.category_iter)
        return current
    
    def __iter__(self):
        return self

class category_iterator:
    def __init__(self, catalog, category):
        self.category = category
        super_list = mp.valueSet(catalog.videos)
        self.super_iter = lliterator.newIterator(super_list)
        country_map = lliterator.next(self.super_iter)
        category_list = mp.get(country_map, category)['value']
        self.category_iter = aliterator.newIterator(category_list)
    
    def __next__(self):
        while not aliterator.hasNext(self.category_iter):
            if not lliterator.hasNext(self.super_iter):
                raise StopIteration
            else:
                country_map = lliterator.next(self.super_iter)
                category_list = mp.get(country_map, self.category)['value']
                self.category_iter = aliterator.newIterator(category_list)
        current = aliterator.next(self.category_iter)
        return current
    
    def __iter__(self):
        return self

class video_catalog:
    # Funciones para agregar informacion al catalogo
    def add_video(self, line):
        if line:
            categories = lt.newList(datastructure='ARRAY_LIST')
            tags = lt.newList()
            i = 0
            for element in line.items():
                if (i <=10 and 7 <= i) or i ==4:
                    lt.addLast(categories, int(element[1]))
                elif i != 6:
                    lt.addLast(categories, element[1])
                else:
                    tagl = element[1].replace('"', '').split('|')
                    for tag in tagl:
                        lt.addLast(tags, tag)
                i += 1
            country_map_pair = mp.get(self.videos, lt.getElement(categories, 16))
            if country_map_pair:
                country_map = country_map_pair['value']
            else:
                country_map = mp.newMap(numelements=43)
                mp.put(self.videos, lt.getElement(categories, 16), country_map)
            category_list_pair = mp.get(country_map, lt.getElement(categories, 5))
            if category_list_pair:
                category_list = category_list_pair['value']
            else:
                category_list = lt.newList(datastructure='ARRAY_LIST')
                mp.put(country_map, lt.getElement(categories, 5), category_list)
            lt.addLast(category_list, (categories, tags))
    
    # Construccion de modelos
    def add_videos(self, filepath: str):
        if filepath is not None:
            input_file = csv.DictReader(open(filepath, encoding="utf-8"),
                                        delimiter=',')
            size = 20
            self.videos = mp.newMap(numelements=size)
            for line in input_file:
                self.add_video(line)

    def add_tags(self, filepath, type="ARRAY_LIST"):
        self.tags=lt.newList(type)
        data= open(filepath)
        data.readline()
        linea= data.readline().replace("\n","").split("\t")
        while len(linea)>1:
            lt.addLast(self.tags,linea)
            linea=data.readline().replace("\n","").split("\t")

    def __init__(self, filepath_videos: str, filepath_tags: str):
        self.videos = None
        self.add_videos(filepath_videos)
        self.tags = None
        self.add_tags(filepath_tags)
    
    def __iter__(self):
        return catalog_iterator(self)

    def req_1(self, country: str, category: int, n: int):
        top = lt.newList()
        for video in country_category_iterator(self, country, category):
             if_add_video_req(video, top, 7, n)
        return top

    def req_2(self, country:str):
        repeticiones = mp.newMap(numelements=20000)
        for video in country_iterator(self, country):
            video_id = lt.getElement(video[0], 1)
            video_pair = mp.get(repeticiones, video_id)
            if video_pair:
                mp.put(repeticiones, video_id, (video, video_pair['value'][1]+1))
            else:
                mp.put(repeticiones, video_id, (video, 1))
        videos_ids = mp.keySet(repeticiones)
        id_iter = lliterator.newIterator(videos_ids)
        maximo = 0
        max_id = 0
        while lliterator.hasNext(id_iter):
            video_id = lliterator.next(id_iter)
            video = mp.get(repeticiones, video_id)['value']
            video_rep = video[1]
            if video_rep > maximo:
                maximo = video_rep
                max_id = video_id
        res = lt.newList()
        res_vid = mp.get(repeticiones, video_id)['value']
        lt.addFirst(res, res_vid[0])
        return (res, res_vid[1])
    
    def req_3(self, category:str):
        repeticiones = mp.newMap(numelements=20000)
        for video in category_iterator(self, category):
            video_id = lt.getElement(video[0], 1)
            video_pair = mp.get(repeticiones, video_id)
            if video_pair:
                mp.put(repeticiones, video_id, (video, video_pair['value'][1]+1))
            else:
                mp.put(repeticiones, video_id, (video, 1))
        videos_ids = mp.valueSet(repeticiones)
        id_iter = lliterator.newIterator(videos_ids)
        maximo = 0
        max_vid = 0
        while lliterator.hasNext(id_iter):
            video = lliterator.next(id_iter)
            video_rep = video[1]
            if video_rep > maximo:
                maximo = video_rep
                max_vid = video[0]
        res = lt.newList()
        res_vid = mp.get(repeticiones, video_id)['value']
        lt.addFirst(res, res_vid[0])
        return (res, res_vid[1])

    def req_4(self, country: str, tag:str, n: int):
        top = lt.newList()
        for video in country_iterator(self, country):
            if lt.isPresent(video[1], tag):
                if_add_video_req(video, top, 8, n)
        return top




# Funciones para creacion de datos



# Funciones de consulta



def has_tag(videos, id, tag):
    return lt.isPresent(mp.get(videos, id), tag)

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

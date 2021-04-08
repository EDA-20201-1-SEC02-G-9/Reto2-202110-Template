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

def add_to_top(video, top):
    iter_video = top['first']
    while iter_video['next'] and lt.getElement(video[0], 8) > lt.getElement(iter_video['next']['info'][0], 8):
        iter_video = iter_video['next']
    next = iter_video['next']
    iter_video['next'] = {'info': video, 'next': next}
    if not next:
        top['last'] = iter_video['next']
    top['size'] += 1

def if_add_video_req_4(video, top, category: int, n: int):
    if lt.getElement(video[0], 5) == category:
        print(lt.getElement(video[0], 8))
        min_top = None
        if not lt.isEmpty(top):
            min_top = lt.firstElement(top)
        if not min_top:
            lt.addFirst(top, video)
        # ... or likesVideo > likesMinTop:
        elif lt.size(top) < n or lt.getElement(video[0], 8) > lt.getElement(min_top[0], 8):
            add_to_top(video, top)
        print(lt.size(top))
        if lt.size(top) > n:
            lt.removeFirst(top)

class catalog_iterator:
    def __init__(self, catalog):
        super_list = mp.valueSet(catalog.videos)
        self.super_iter = lliterator.newIterator(super_list)
        self.especific_iter = aliterator.newIterator(lliterator.next(self.super_iter))

    
    def __next__(self):
        while not aliterator.hasNext(self.especific_iter):
            if not lliterator.hasNext(self.super_iter):
                raise StopIteration
            else:
                self.especific_iter = aliterator.newIterator(lliterator.next(self.super_iter))
        current = aliterator.next(self.especific_iter)
        return current

class video_catalog:
    # Funciones para agregar informacion al catalogo
    def add_video(self, line):
        if line:
            categories = lt.newList(datastructure='ARRAY_LIST')
            tags = lt.newList()
            for element in line.items():
                if element[0] in ['likes','dislikes','views','comment_count','category_id']:
                    lt.addLast(categories, int(element[1]))
                elif element[0] != 'tags':
                    lt.addLast(categories, element[1])
                else:
                    tagl = element[1].replace('"', '').split('|')
                    for tag in tagl:
                        lt.addLast(tags, tag)
            country_list_pair = mp.get(self.videos, lt.getElement(categories, 16))
            if country_list_pair:
                country_list = country_list_pair[1]
            else:
                country_list = lt.newList(datastructure='ARRAY_LIST')
                mp.put(self.videos, lt.getElement(categories, 15), country_list)
            lt.addLast(country_list, (categories, tags))
    
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

    def req_4(self, category: int, n: int):
        top = lt.newList()
        for video in self:
             if_add_video_req_4(video, top, category, n)
        return top




# Funciones para creacion de datos



# Funciones de consulta



def has_tag(videos, id, tag):
    return lt.isPresent(mp.get(videos, id), tag)

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

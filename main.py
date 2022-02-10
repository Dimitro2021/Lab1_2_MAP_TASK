""" Map creator """

import argparse
from cmath import cos, sin, sqrt
from math import pi
from geopy.geocoders import Nominatim
from numpy import arcsin
import folium


geolocator = Nominatim(user_agent='Google map')


def parse_creation():
    """test"""
    parser = argparse.ArgumentParser(description='help building map')
    parser.add_argument('latitude', default=49.5569324)
    parser.add_argument('longitude', default=49.5569324)
    parser.add_argument('year', default=2000)
    parser.add_argument('path', default=2000)
    return parser.parse_args()

def file_open(path, year):
    """test"""
    with open(path, 'r', errors='ignore', encoding='utf-8') as films:
        while films.readline().find('======') == -1:
            continue
        all_flms = []
        all_flms = [(film.split('(')[0][:-1], film.split('\t')[-2] if film.endswith(')\n') \
else film.split('\t')[-1][:-1])for film in films if f'({year})' in film]
    return all_flms

def length(coords1, coords2):
    """calculate distance"""
    if None in coords1:
        return -1
    try:
        r_const = 6371000
        f1_const, f2_const = coords1[0]*pi/180, coords2[0]*pi/180
        df_const = (coords2[0]-coords1[0])*pi/180
        da_const = (coords2[1]-coords1[1])*pi/180
        a_const = sin(df_const/2)**2+cos(f1_const)*cos(f2_const)*sin(da_const/2)**2
        c_const = 2*r_const*arcsin(sqrt(a_const))
        return 0 if c_const == 0j else int(str(c_const).split('.', maxsplit=1)[0][1:])
    except TypeError:
        print(':)')
        return -1

FIL_LOC = {}

def coords_place(film: tuple):
    """coordinates of place"""
    if film in FIL_LOC:
        return FIL_LOC[film]
    try:
        location = geolocator.geocode(film)
        if location is None:
            flag = (None, None)
        else:
            flag = FIL_LOC[film] = location.latitude, location.longitude
    except TimeoutError:
        print('Time error(')
    return flag

def list_cords(films: list, coords: tuple):
    """Sort by length"""
    films = [(film[0], coords_place(film[1])) for film in films]
    films.sort(key=lambda x: length(x[1], coords))
    return films

def creation(films: list, location: tuple, year: str):
    """ map creator """
    mapp = folium.Map(location=location, zoom_control=10)
    featg = folium.FeatureGroup(name=f'films from year {year}')
    kol = 0
    usd_coords = usd_flms = []
    for film in films:
        if kol > 9:
            break
        if None not in film[1]:
            constt = usd_coords.count(film[1])
            coords = [film[1][0]+0.001*((-1)**(constt%2))*constt*(constt%2), \
        film[1][1]+0.001*((-1)**((constt+1)%2))*constt*((constt+1)%2)]
            featg.add_child(folium.Marker(location=coords,
                                          popup=film[0]+str(usd_flms.count(film[0])+1),
                                          icon=folium.Icon()))
            usd_flms.append(film[0])
            usd_coords.append(location)
            kol = kol+1
    mapp.add_child(featg)
    featg2 = folium.FeatureGroup(name='One more shar!!')
    featg2.add_child(folium.Marker(location=[45.8131847, 15.9771774],
                                popup='Lijepa nasa ovdje',
                                icon=folium.Icon()))
    featg2.add_child(folium.Marker(location=[50.4500336, 30.5241361],
                                   popup='А Київ тут',
                                   icon=folium.Icon()))
    mapp.add_child(featg2)
    mapp.add_child(folium.LayerControl())
    mapp.save('Map with films.html')


def main():
    """ Collect all info and do everythiiing """
    try:
        args = parse_creation()
        coords, year, path = (float(args.latitude), float(args.longitude)), args.year, args.path
        films = list_cords(file_open(path, year), coords)
        if len(films) == 0:
            print('No film in this date')
        creation(films, coords, year)
    except Exception as err:
        print(f'{err} happaned')
main()

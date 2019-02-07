#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 14:27:36 2019

@author: s1881079
"""
import numpy as np
import cx_Oracle
import pandas as pd
import json
import pyproj
#from jinja2 import Environment, FileSystemLoader


class Point:
    def __init__(self,r_x,r_y):
        self.x = r_x
        self.y = r_y

    def toLatLon(self):
        wgs84=pyproj.Proj("+init=EPSG:4326")
        map_proj = pyproj.Proj("+init=EPSG:3857")
        lon,lat = pyproj.transform(map_proj,wgs84, self.x, self.y)
        self.x = lon
        self.y = lat

    def getLatLon(self):
        self.toLatLon()
        return [self.x,self.y]
    
    def coorToGeoJson(self):
        return {'type' : 'Point',
                'coordinates':[self.x,self.y]}


class StartPoint(Point):
    def __init__(self,r_id,r_x,r_y):
        self.id = r_id
        self.x = r_x
        self.y = r_y
        
    def toGeoJson(self):
        return {'type' : 'Feature',
                'properties' : {
                        'start_id' : self.id
                        },
                'geometry':self.coorToGeoJson()}

class PointSeqs(list):
    def __init__(self,ar_x=[],ar_y=[]):
        c_point = len(ar_x)
        for i in range(c_point):
            self.append(Point(i,ar_x[i],ar_y[i]))
        
    def coorArrToGeoJson(self):
        coor_list = []
        for pt in self:
            coor_list.append(pt.getLatLon())
        return coor_list

class ZonePolygon(PointSeqs):
    
    def __init__(self,zone_id,ar_x=[],ar_y=[]):
        self.id = zone_id
        c_point = len(ar_x)
        for i in range(c_point):
            self.append(Point(ar_x[i],ar_y[i]))
            
    def toGeoJson(self):
        return {'type' : 'Feature',
                'properties' : {
                        'zone_id' : self.id
                        },
                'geometry':{
                        'type' : 'Polygon',
                        'coordinates' : [self.coorArrToGeoJson()]
                        }}


def connect_dbs():
    '''
    connect to database
    '''
    try:
        conn = cx_Oracle.connect("s1889111/Muffle67@geosgen")
    except:
        print('Cannot link to database')
        return None

    return conn


def grab_info(table_key):
    '''
    return sql plus command according to keyword
    '''
    qy_switcher = {
            'get_start_pts' : 'select c.startpoint_id, t.X, t.Y from s1889111.startpoints c, TABLE(SDO_UTIL.GETVERTICES(c.geom)) t',
            'get_zone_polygons_pts' : 'select c.zone_id, t.x, t.y from s1889111.zones c, table(sdo_util.getvertices(c.geom)) t'
            'get_treasure_pts' : 'select c.penalty_id, t.x, t.y from s1889111.treasure c, table(sdo_util.getvertices(c.geom)) t'
            'get_link_pts' : 'select c.path_id, t.x, t.y from s1889111.path c, table(sdo_util.getvertices(c.geom)) t'
            'get_risk_pts' : 'select c.risk_id, t.x, t.y from s1889111.risks c, table(sdo_util.getvertices(c.geom)) t'
            }

    return qy_switcher.get(table_key)


def getStartPtsJson(cs):
    '''
    generate GeoJson for startpoints
    '''
    points_json_list = []
    for pt in cs:
        stpt = StartPoint(pt[0],pt[1],pt[2])
        stpt.toLatLon()
        points_json_list.append(stpt.toGeoJson())

    return json.dumps(points_json_list)

def getZonePolyJson(cs):
    '''
    generate GeoJson for zones
    '''
    list_rec = []
    for row in cs:
        list_rec.append([row[0],row[1],row[2]])
        
    df = pd.DataFrame(list_rec, columns = ['zone_id','x','y'])
    xs_list = []
    ys_list = []
    zoneid_list = []
    for zone_id, pt in df.groupby('zone_id'):
        zoneid_list.append(zone_id)
        xs_list.append(pt.x)
        ys_list.append(pt.y)
        
    zones_json_list = []
    for i in range(len(zoneid_list)):
        zones_json_list.append(ZonePolygon(zoneid_list[i],np.array(xs_list[i]),np.array(ys_list[i])).toGeoJson())

    return json.dumps(zones_json_list)
    
    
def formObjectJson(cs,table_key):
    '''
    return geoJson according to object type
    '''
    if table_key == 'get_start_pts':
        rst_json = getStartPtsJson(cs)
    if table_key == 'get_zone_polygons_pts':
        rst_json = getZonePolyJson(cs)
    return rst_json

def getInfoFromDB(conn,table_key):
    '''
    extract information from database
    '''
    qy_expr = grab_info(table_key)
    cs = conn.cursor()
    cs.execute(qy_expr)
    
    rst = formObjectJson(cs,table_key)
    
    return rst

if __name__ == '__main__':
    conn = connect_dbs()
    start_pt_geojson = getInfoFromDB(conn,'get_start_pts')
    zones_geojson = getInfoFromDB(conn,'get_zone_polygons_pts')
    treasure_geojson = getInfoFromDB(conn,'get_treasure_pts')
    links_geojson = getInfoFromDB(conn,'get_link_pts')
    risks_geojson = getInfoFromDB(conn,'get_risk_pts')
    
#JINJA
#    env = Environment(loader = FileSystemLoader('template'))
#    template = env.get_template('playground.html')
#    print('Content-Type: text/html\n')
#    print(template.render(
#        zones_json = zones_geojson,
#        stpts_json = start_pt_geojson
#    ))

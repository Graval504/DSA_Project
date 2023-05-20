from __future__ import annotations
from typing import *
import pandas as pd
import math
from copy import deepcopy

def a_star_yen(graph:Dict[str,Dict[str,List]], start:str, end:str, K:int = 1) -> List[Tuple[list,int]]:
    result = []
    close_list = _a_star(graph,start,end)
    path:List[Subway_node] = []
    node = close_list[-1]
    result.append((node.get_path(),node.cost))
    while node.parent != None:
        path.append(node)
        node = node.parent
    path.sort(key= lambda x:x.cost-x.parent.cost)

    for node in path:
        if K <= 1:
            result.sort(key=lambda x:x[1])
            return result
        data = deepcopy(graph)
        for station in data[node.parent.station][node.parent.line]:
            if station[0] == node.station:
                data[node.parent.station][node.parent.line].remove(station)
                break
        added_path = _a_star(data,start,end)[-1]
        appended = (added_path.get_path(),added_path.cost)
        if not appended in result:
            result.append(appended)
            K -= 1
        
    result.sort(key=lambda x:x[1])
    return result

def _a_star(graph:Dict[str,Dict[str,List]], start:str, end:str) -> List[Subway_node]:
    open_list:List[Subway_node] = []
    close_list:List[Subway_node] = []
    arrival = False
    close_list.append(Subway_node(list(graph[start].keys())[0],start,end))
    
    while not arrival:
        for node in close_list[-1].get_neighbors(graph):
            new_node = Subway_node(node[1],node[0],end,node[2],close_list[-1])
            
            if has_station(close_list,new_node):
                continue
            openstation = has_station(open_list,new_node)
            if openstation and new_node.score < openstation.score:
                openstation.update_node(new_node)
                continue
            if not openstation:
                open_list.append(new_node)
        min_score_node = open_list[0]
        for node in open_list[1:]:
            if node.score < min_score_node.score:
                min_score_node = node
        open_list.remove(min_score_node)
        close_list.append(min_score_node)
        if close_list[-1].station == end:
            arrival = True
    return close_list

class Subway_node():
    location_sheet = pd.read_csv("subway_location.csv",header=None)
    def __init__(self,line:str,station:str,end:str,cost:int=0,parent_node:Subway_node|None=None):
        self.parent = parent_node
        self.score = 0
        self.cost = cost
        if type(parent_node) == Subway_node:
            self.cost += parent_node.cost
        self.score += cost
        self.line = line
        self.station = station
        self.score += self.get_subway_distance(end)

    def get_path(self) -> list:
        result = []
        result.append((self.line,self.station))
        parent = self.parent
        while parent != None:
            result.append((parent.line,parent.station))
            parent = parent.parent
        result = result[::-1]
        if result[0][1] == result[1][1]:
            result.pop(0)
        return result
    
    def update_node(self,updated_node:Subway_node):
        self.parent = updated_node.parent
        self.score = updated_node.score
        self.cost = updated_node.cost
    
    def get_subway_distance(self, end:str) -> float: 
        station1_location = Subway_node.location_sheet[(Subway_node.location_sheet[0] == int(self.line[-1])) & (Subway_node.location_sheet[1] == self.station)]
        try:
            lat1 = station1_location[2].values[0]
            lon1 = station1_location[3].values[0]
            station2_location = Subway_node.location_sheet[Subway_node.location_sheet[1] == end].head(1)
            lat2 = station2_location[2].values[0]
            lon2 = station2_location[3].values[0]
            lat1,lat2,lon1,lon2 = map(math.radians,[lat1,lat2,lon1,lon2])
        except:
            print(self.station,self.line,end)
            raise
        distance = math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1-lon2)
        distance = math.acos(distance)
        distance *= 6371 # 지구 평균 반지름
        return distance
    
    def get_neighbors(self,graph) -> List[Tuple[str,str,int]]:
        return graph[self.station][self.line]

def has_station(station_list:List[Subway_node],target_station:Subway_node) -> Subway_node|None:
    for station in station_list:
        if station.station == target_station.station and station.line == target_station.line:
            return station
    return None

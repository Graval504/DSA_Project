import json

# set INF value
INF = 9999999

# bellman-ford algorithm
def bellman_ford(graph, start, end):
    # init
    dist = {(station, line) : INF if station != start else 0 for station in graph.keys() for line in graph[station].keys()}
    parent = {(station, line) : None for station in graph.keys() for line in graph[station].keys()}

    # caculate distance
    n = len(dist)
    for _ in range(n - 1):
        for parent_station in dist.keys():
            for station, line, cost in graph[parent_station[0]][parent_station[1]]:
                child_station = (station, line)
                if dist[child_station] > dist[parent_station] + cost:
                    dist[child_station]  = dist[parent_station] + cost
                    parent[child_station] = parent_station


    min_cost = INF
    min_line = None
    for line in graph[end].keys():
        if dist[(end, line)] < min_cost:
            min_cost = dist[(end, line)]
            min_line = line
            
    
    node = (end, min_line)
    path = []
    while node[0] != start:
        path.append(node)
        node = parent[node]
    path.append(node)
    path.reverse()

    return min_cost, path

filename = ["equal","unequal","real"]
index = int(input("0 : 역간 거리 동일, 1 : 역간 거리 무작위, 2: 역간 거리 실제 반영\n역간거리:"))
with open(f'subway({filename[index]}).json', 'r', encoding='utf-8') as f:
    data = json.load(f)

start = input('출발지: ')
end = input('도착지: ')

result = bellman_ford(data, start, end)

print('소요시간:', result[0])

print(start, end='')
cur_line = result[1][0][1]
for index, data in enumerate(result[1]):
    if data[0] == start: continue
    print('(환승)' if cur_line != data[1] else '-%s' % data[0], end='')
    cur_line = data[1]

print()
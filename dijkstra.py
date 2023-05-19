import json
import heapq

# set INF value
INF = 9999999

# dijkstra algorithm
def dijkstra(graph, start, end):
    # init
    dist = {station : {line : INF for line in graph[station]} for station in graph}
    paths = {(start, line) : [(start, line, 0)] for line in graph[start]}

    # insert start nodes into heap
    heap = []
    for line in graph[start]:
        heapq.heappush(heap, (0, start, line))
        dist[start][line] = 0
    
    while heap:
        # pop min node
        cur_dist, cur_station, cur_line = heapq.heappop(heap)
        
        # check if 'cur_dist' is min
        if dist[cur_station][cur_line] < cur_dist:
            continue

        # search adjacency nodes
        for nxt_station, nxt_line, cost in graph[cur_station][cur_line]:
            new_dist = cur_dist + cost

            # update dist & path
            if new_dist < dist[nxt_station][nxt_line]:
                dist[nxt_station][nxt_line] = new_dist
                paths[(nxt_station, nxt_line)] = paths[(cur_station, cur_line)] + [(nxt_station, nxt_line, cost)]
                heapq.heappush(heap, (new_dist, nxt_station, nxt_line))
    
    # return result
    min_line, min_cost = min(dist[end].items(), key=lambda x: x[1])
    return min_cost, paths[(end, min_line)]


filename = ["equal","unequal","real"]
index = int(input("0 : 역간 거리 동일, 1 : 역간 거리 무작위, 2: 역간 거리 실제 반영\n역간거리:"))
with open(f'subway({filename[index]}).json', 'r', encoding='utf-8') as f:
    data = json.load(f)

start = input('출발지: ')
end = input('도착지: ')

result = dijkstra(data, start, end)

print('소요시간:', result[0])

print(start, end='')
cur_line = result[1][0][1]
for index, data in enumerate(result[1]):
    if data[0] == start: continue
    print(f"({cur_line[-1]}->{data[1][-1]} 환승)" if cur_line != data[1] else '-%s' % data[0], end='')
    cur_line = data[1]

print()
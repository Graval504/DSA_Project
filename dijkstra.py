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


with open('subway(unequal).json', 'r', encoding='utf-8') as f:
    data = json.load(f)

start = input('출발지: ')
end = input('도착지: ')

result = dijkstra(data, start, end)
print(result)
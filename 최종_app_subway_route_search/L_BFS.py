from queue import Queue

def bfs(graph, start, end):
    visited = []                # 방문처리에 사용
    queue = Queue()             
    
    for line in graph[start]:   
        queue.put((start, line,[[start,line,0]]))  #정점을 큐에 넣는다.
        visited.append((start, line))  #정점을 방문 처리한다.

    while not queue.empty():
        STATION = queue.get()
        node, line, path = STATION  #역, 호선번호, 경로
        if node == end:  
            return path

        
        for item in graph[node][line]:
            station_info = (item[0], item[1])
            if  station_info in visited: #방문한 노드 검사
                continue
            new_path = path + [item]  # 경로에 다음 역 추가
            queue.put((item[0], item[1], new_path))
            visited.append(station_info)
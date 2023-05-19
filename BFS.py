''' BFS 구현'''
from queue import Queue
import json

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

#-- 결과 출력부 --#
filename = ["equal","real"]
index = int(input("<숫자입력하여 데이터세트 선택> (0=제공한 원본 데이터) (1=실제 역간 소요시간 반영) \n")) #데이터 세트 선택 옵션
with open(f'subway({filename[index]}).json', 'r', encoding='utf-8') as f:
    data = json.load(f)

start = input('출발지: ')
end = input('도착지: ')

#--------------------------------#
result = bfs(data, start, end)
print('출발역: ','%s호선' %result[0][1], result[0][0],)
print('총 소요시간: %s분'% (2*(len(result)-1)))
print('경로 : ',end='')
print("(%s %s)"%(result[0][0],result[0][1][-1]), end=' ')

current_line = result[0][1][-1]
for index, data in  enumerate(result):
    if data[0] == start: continue
    if current_line != data[1][-1] : print("[%s -> %s호선 환승] "%(current_line,data[1][-1]),end='') # 환승처리

    print("(%s %s)"%(data[0],data[1][-1]), end=' ') #역 및 호선 출력
    current_line = data[1][-1]